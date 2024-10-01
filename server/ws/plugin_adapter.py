from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from typing import List, Dict, Any
import logging
from pydantic import BaseModel
import time
from collections import defaultdict
from threading import Lock

app = FastAPI()
logger = logging.getLogger("plugin_adapter")

# Constants
WEBSOCKET_MESSAGE_PREFIX = "custom_focalboard_"
STALE_THRESHOLD = 300  # 5 minutes in seconds

# Error
class MissingTeamError(Exception):
    pass

# Data Models
class WebSocketRequest(BaseModel):
    action: str
    data: Dict[str, Any]

class WebsocketCommand(BaseModel):
    action: str
    team_id: str
    read_token: str = None
    block_ids: List[str] = []

# Plugin Adapter Client
class PluginAdapterClient:
    def __init__(self, web_conn_id: str, user_id: str):
        self.web_conn_id = web_conn_id
        self.user_id = user_id
        self.inactive_at = 0
        self.teams = []
        self.blocks = []

    def is_active(self):
        return (time.time() - self.inactive_at) < STALE_THRESHOLD

    def has_expired(self):
        return (time.time() - self.inactive_at) >= STALE_THRESHOLD

# Plugin Adapter
class PluginAdapter:
    def __init__(self):
        self.listeners: Dict[str, PluginAdapterClient] = {}
        self.listeners_by_user_id: Dict[str, List[PluginAdapterClient]] = defaultdict(list)
        self.listeners_by_team: Dict[str, List[PluginAdapterClient]] = defaultdict(list)
        self.lock = Lock()

    def add_listener(self, pac: PluginAdapterClient):
        with self.lock:
            self.listeners[pac.web_conn_id] = pac
            self.listeners_by_user_id[pac.user_id].append(pac)

    def remove_listener(self, pac: PluginAdapterClient):
        with self.lock:
            # Remove listener from team subscriptions
            for team in pac.teams:
                self.listeners_by_team[team].remove(pac)

            # Remove listener from user list
            self.listeners_by_user_id[pac.user_id].remove(pac)
            del self.listeners[pac.web_conn_id]

    def get_listener_by_web_conn_id(self, web_conn_id: str) -> PluginAdapterClient:
        return self.listeners.get(web_conn_id)

    def web_socket_message_has_been_posted(self, web_conn_id: str, user_id: str, req: WebSocketRequest):
        pac = self.get_listener_by_web_conn_id(web_conn_id)
        if pac is None:
            logger.debug(f"Received a message for an unregistered webconn: {web_conn_id}, user: {user_id}")
            return

        if not req.action.startswith(WEBSOCKET_MESSAGE_PREFIX):
            return

        command = self.command_from_request(req)
        if command is None:
            return

        # Handle commands
        if command.action == "subscribe_team":
            self.subscribe_listener_to_team(pac, command.team_id)
        elif command.action == "unsubscribe_team":
            self.unsubscribe_listener_from_team(pac, command.team_id)

    def command_from_request(self, req: WebSocketRequest) -> WebsocketCommand:
        team_id = req.data.get("teamId")
        if not team_id:
            raise MissingTeamError("Command doesn't contain teamId")
        
        return WebsocketCommand(
            action=req.action[len(WEBSOCKET_MESSAGE_PREFIX):],
            team_id=team_id,
            read_token=req.data.get("readToken"),
            block_ids=req.data.get("blockIds", [])
        )

    def subscribe_listener_to_team(self, pac: PluginAdapterClient, team_id: str):
        if team_id not in pac.teams:
            self.listeners_by_team[team_id].append(pac)
            pac.teams.append(team_id)

    def unsubscribe_listener_from_team(self, pac: PluginAdapterClient, team_id: str):
        if team_id in pac.teams:
            self.listeners_by_team[team_id].remove(pac)
            pac.teams.remove(team_id)

# Global PluginAdapter instance
plugin_adapter = PluginAdapter()

# WebSocket endpoint
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    web_conn_id = str(id(websocket))  # Example to generate a unique ID
    plugin_adapter.add_listener(PluginAdapterClient(web_conn_id, user_id))

    try:
        while True:
            data = await websocket.receive_text()
            request_data = WebSocketRequest.parse_raw(data)
            plugin_adapter.web_socket_message_has_been_posted(web_conn_id, user_id, request_data)
    except WebSocketDisconnect:
        plugin_adapter.remove_listener(plugin_adapter.get_listener_by_web_conn_id(web_conn_id))

