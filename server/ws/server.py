import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketDisconnect
from typing import List, Dict, Any, Union
import logging

# Set up logging
logger = logging.getLogger(__name__)

class WebSocketSession:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.user_id: str = ""
        self.teams: List[str] = []
        self.blocks: List[str] = []

    async def send_json(self, data: Any):
        await self.websocket.send_json(data)

    def is_authenticated(self) -> bool:
        return bool(self.user_id)

class WebSocketServer:
    def __init__(self):
        self.active_connections: Dict[str, WebSocketSession] = {}
        self.listeners_by_team: Dict[str, List[WebSocketSession]] = {}
        self.listeners_by_block: Dict[str, List[WebSocketSession]] = {}
        self.auth = None  # Implement your authentication logic here
        self.single_user_token = ""  # Set your single user token here
        self.is_mattermost_auth = False

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        session = WebSocketSession(websocket)
        self.active_connections[session.user_id] = session

    async def disconnect(self, session: WebSocketSession):
        del self.active_connections[session.user_id]
        for team in session.teams:
            self.remove_listener_from_team(session, team)
        for block in session.blocks:
            self.remove_listener_from_block(session, block)

    async def handle_message(self, session: WebSocketSession, message: str):
        command = json.loads(message)
        action = command.get("action")

        if action == "auth":
            await self.authenticate_listener(session, command.get("token"))
        elif action == "subscribe_team":
            await self.subscribe_listener_to_team(session, command.get("team_id"))
        elif action == "unsubscribe_team":
            await self.unsubscribe_listener_from_team(session, command.get("team_id"))
        elif action == "subscribe_blocks":
            await self.subscribe_listener_to_blocks(session, command.get("block_ids"))
        elif action == "unsubscribe_blocks":
            await self.unsubscribe_listener_from_blocks(session, command.get("block_ids"))
        else:
            logger.error(f"Invalid action: {action}")

    async def authenticate_listener(self, session: WebSocketSession, token: str):
        # Implement your authentication logic here
        logger.debug(f"Authenticating session with token: {token}")
        session.user_id = self.get_user_id_for_token(token)
        if session.user_id:
            logger.debug(f"Session authenticated for user: {session.user_id}")

    async def subscribe_listener_to_team(self, session: WebSocketSession, team_id: str):
        if team_id in session.teams:
            return
        session.teams.append(team_id)
        if team_id not in self.listeners_by_team:
            self.listeners_by_team[team_id] = []
        self.listeners_by_team[team_id].append(session)

    async def unsubscribe_listener_from_team(self, session: WebSocketSession, team_id: str):
        if team_id not in session.teams:
            return
        session.teams.remove(team_id)
        if team_id in self.listeners_by_team:
            self.listeners_by_team[team_id].remove(session)

    async def subscribe_listener_to_blocks(self, session: WebSocketSession, block_ids: List[str]):
        for block_id in block_ids:
            if block_id in session.blocks:
                continue
            session.blocks.append(block_id)
            if block_id not in self.listeners_by_block:
                self.listeners_by_block[block_id] = []
            self.listeners_by_block[block_id].append(session)

    async def unsubscribe_listener_from_blocks(self, session: WebSocketSession, block_ids: List[str]):
        for block_id in block_ids:
            if block_id in session.blocks:
                session.blocks.remove(block_id)
                self.listeners_by_block[block_id].remove(session)

    def get_user_id_for_token(self, token: str) -> str:
        if self.single_user_token and token == self.single_user_token:
            return "single_user_id"
        # Implement session retrieval logic here
        return ""

app = FastAPI()
server = WebSocketServer()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await server.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            session = server.active_connections.get(websocket)
            await server.handle_message(session, data)
    except WebSocketDisconnect:
        await server.disconnect(session)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List, Dict
import logging

app = FastAPI()

# Define logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define models for messages (replace these with your actual data models)
class Block:
    def __init__(self, id: str, parent_id: str, board_id: str):
        self.id = id
        self.parent_id = parent_id
        self.board_id = board_id

class UpdateBlockMsg:
    def __init__(self, action: str, team_id: str, block: Block):
        self.action = action
        self.team_id = team_id
        self.block = block

class Listener:
    def __init__(self, websocket: WebSocket):
        self.conn = websocket

# In-memory storage for listeners
listeners: Dict[str, List[Listener]] = {}

# WebSocket connection endpoint
@app.websocket("/ws/{team_id}")
async def websocket_endpoint(websocket: WebSocket, team_id: str):
    await websocket.accept()
    if team_id not in listeners:
        listeners[team_id] = []
    
    listener = Listener(websocket)
    listeners[team_id].append(listener)
    logger.info(f"New connection for team_id: {team_id}")

    try:
        while True:
            # Here you can handle incoming messages from the client if needed
            data = await websocket.receive_text()
            logger.debug(f"Received data: {data}")
    except WebSocketDisconnect:
        listeners[team_id].remove(listener)
        logger.info(f"Disconnected from team_id: {team_id}")

# Broadcast function for blocks
async def broadcast_block_change(team_id: str, block: Block):
    message = UpdateBlockMsg(action="update_block", team_id=team_id, block=block)

    for listener in listeners.get(team_id, []):
        logger.debug(f"Broadcasting block change to {listener.conn}")
        try:
            await listener.conn.send_json(message.__dict__)
        except Exception as e:
            logger.error(f"Broadcast error: {e}")
            await listener.conn.close()

# Example endpoint to trigger block change broadcasting
@app.post("/broadcast_block_change/{team_id}")
async def trigger_broadcast_block_change(team_id: str, block_id: str, parent_id: str):
    block = Block(id=block_id, parent_id=parent_id, board_id="example_board_id")  # Replace with your logic
    await broadcast_block_change(team_id, block)
    return {"message": "Broadcast initiated."}

# Add similar functions for other broadcasting scenarios like categories, boards, etc.
