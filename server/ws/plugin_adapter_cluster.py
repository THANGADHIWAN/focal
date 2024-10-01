import json
import logging
from typing import List, Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI

# Set up logging
logger = logging.getLogger("PluginAdapter")
logger.setLevel(logging.DEBUG)

class ClusterMessage(BaseModel):
    team_id: str
    board_id: str
    user_id: str
    payload: Dict[str, Any]
    ensure_users: List[str] = []

class PluginAdapter:
    def __init__(self, api):
        self.api = api  # Assuming some API instance is passed to handle messaging/publishing.

    def send_message_to_cluster(self, cluster_message: ClusterMessage):
        id = "websocket_message"
        try:
            # Serializing cluster message to JSON
            b = json.dumps(cluster_message.dict())
        except Exception as err:
            logger.error(f"couldn't get JSON bytes from cluster message: {err}")
            return

        # Create event to send (assuming some sort of pub-sub mechanism is available)
        event = {
            "id": id,
            "data": b
        }
        opts = {
            "send_type": "reliable"  # Assuming we implement reliable sending
        }

        # Simulating PublishPluginClusterEvent
        try:
            self.api.publish_plugin_cluster_event(event, opts)
        except Exception as err:
            logger.error(f"Error publishing cluster event: {err}")

    def handle_cluster_event(self, ev: Dict[str, Any]):
        logger.debug(f"received cluster event: {ev['id']}")

        try:
            # Deserializing the event data
            cluster_message = ClusterMessage(**json.loads(ev['data']))
        except Exception as err:
            logger.error(f"Cannot unmarshal cluster message data: {err}")
            return

        if cluster_message.board_id:
            # Simulating sendBoardMessageSkipCluster method
            self.send_board_message_skip_cluster(
                cluster_message.team_id, 
                cluster_message.board_id, 
                cluster_message.payload, 
                *cluster_message.ensure_users
            )
            return

        action = cluster_message.payload.get("action", "")
        if not action:
            logger.warning(f"Cannot determine action from cluster message data: {cluster_message.payload}")
            return

        if cluster_message.user_id:
            # Simulating sendUserMessageSkipCluster method
            self.send_user_message_skip_cluster(action, cluster_message.payload, cluster_message.user_id)
        else:
            # Simulating sendTeamMessageSkipCluster method
            self.send_team_message_skip_cluster(action, cluster_message.team_id, cluster_message.payload)

    def send_board_message_skip_cluster(self, team_id, board_id, payload, *ensure_users):
        logger.debug(f"Sending board message to team {team_id}, board {board_id}, users: {ensure_users}")
        # Implement the logic for sending board message

    def send_user_message_skip_cluster(self, action, payload, user_id):
        logger.debug(f"Sending user message to user {user_id} with action {action}")
        # Implement the logic for sending user message

    def send_team_message_skip_cluster(self, action, team_id, payload):
        logger.debug(f"Sending team message to team {team_id} with action {action}")
        # Implement the logic for sending team message


# FastAPI setup
app = FastAPI()

@app.post("/cluster-event/")
async def handle_cluster_event(event: Dict[str, Any]):
    # Initialize PluginAdapter with an API (stubbed here)
    api = None  # Replace with your actual API handler for messaging
    plugin_adapter = PluginAdapter(api)
    plugin_adapter.handle_cluster_event(event)
    return {"status": "ok"}
