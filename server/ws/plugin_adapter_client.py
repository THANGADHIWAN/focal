import time
from datetime import datetime, timedelta
from typing import List
import threading
import fastapi
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.websockets import WebSocket
from threading import RLock

# Helper function to mimic Go's atomic loading of int64 for inactiveAt
class AtomicInt64:
    def __init__(self, initial_value=0):
        self.value = initial_value
        self.lock = threading.Lock()

    def load(self):
        with self.lock:
            return self.value

    def store(self, new_value):
        with self.lock:
            self.value = new_value

# Mattermost-like time conversion helper (in Go it's mmModel.GetTimeForMillis)
def get_time_for_millis(millis: int):
    return datetime.fromtimestamp(millis / 1000.0)


class PluginAdapterClient:
    def __init__(self, web_conn_id: str, user_id: str):
        self.inactive_at = AtomicInt64(0)  # Atomic variable for inactive timestamp
        self.web_conn_id = web_conn_id
        self.user_id = user_id
        self.teams: List[str] = []
        self.blocks: List[str] = []
        self.lock = RLock()

    def is_active(self) -> bool:
        return self.inactive_at.load() == 0

    def has_expired(self, threshold: timedelta) -> bool:
        return get_time_for_millis(self.inactive_at.load()).timestamp() + threshold.total_seconds() < time.time()

    def subscribe_to_team(self, team_id: str):
        with self.lock:
            self.teams.append(team_id)

    def unsubscribe_from_team(self, team_id: str):
        with self.lock:
            self.teams = [id for id in self.teams if id != team_id]

    def unsubscribe_from_block(self, block_id: str):
        with self.lock:
            self.blocks = [id for id in self.blocks if id != block_id]

    def is_subscribed_to_team(self, team_id: str) -> bool:
        with self.lock:
            return team_id in self.teams

    def is_subscribed_to_block(self, block_id: str) -> bool:
        with self.lock:
            return block_id in self.blocks


# Example FastAPI WebSocket Endpoint
app = FastAPI()

clients = {}

@app.websocket("/ws/{web_conn_id}")
async def websocket_endpoint(websocket: WebSocket, web_conn_id: str):
    client = PluginAdapterClient(web_conn_id, user_id="some-user-id")
    clients[web_conn_id] = client
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            # Process the incoming data, like subscribing to a team/block, etc.
            if data == "subscribe_team":
                client.subscribe_to_team("team_id_example")
            elif data == "unsubscribe_team":
                client.unsubscribe_from_team("team_id_example")
            elif data == "subscribe_block":
                client.subscribe_to_block("block_id_example")
            elif data == "unsubscribe_block":
                client.unsubscribe_from_block("block_id_example")
            
            # Send a message back
            await websocket.send_text(f"Received: {data}")
    except Exception as e:
        # Handle WebSocket disconnection
        print(f"Error: {e}")
    finally:
        del clients[web_conn_id]


# Example REST API endpoint to check subscription status
@app.get("/check_subscription/team/{web_conn_id}/{team_id}")
async def check_team_subscription(web_conn_id: str, team_id: str):
    client = clients.get(web_conn_id)
    if client and client.is_subscribed_to_team(team_id):
        return {"subscribed": True}
    return {"subscribed": False}


@app.get("/check_subscription/block/{web_conn_id}/{block_id}")
async def check_block_subscription(web_conn_id: str, block_id: str):
    client = clients.get(web_conn_id)
    if client and client.is_subscribed_to_block(block_id):
        return {"subscribed": True}
    return {"subscribed": False}
