from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

# WebSocket action constants
WEBSOCKET_ACTION_AUTH = "AUTH"
WEBSOCKET_ACTION_SUBSCRIBE_TEAM = "SUBSCRIBE_TEAM"
WEBSOCKET_ACTION_UNSUBSCRIBE_TEAM = "UNSUBSCRIBE_TEAM"
WEBSOCKET_ACTION_SUBSCRIBE_BLOCKS = "SUBSCRIBE_BLOCKS"
WEBSOCKET_ACTION_UNSUBSCRIBE_BLOCKS = "UNSUBSCRIBE_BLOCKS"
WEBSOCKET_ACTION_UPDATE_BOARD = "UPDATE_BOARD"
WEBSOCKET_ACTION_UPDATE_MEMBER = "UPDATE_MEMBER"
WEBSOCKET_ACTION_DELETE_MEMBER = "DELETE_MEMBER"
WEBSOCKET_ACTION_UPDATE_BLOCK = "UPDATE_BLOCK"
WEBSOCKET_ACTION_UPDATE_CONFIG = "UPDATE_CLIENT_CONFIG"
WEBSOCKET_ACTION_UPDATE_CATEGORY = "UPDATE_CATEGORY"
WEBSOCKET_ACTION_UPDATE_CATEGORY_BOARD = "UPDATE_BOARD_CATEGORY"
WEBSOCKET_ACTION_UPDATE_SUBSCRIPTION = "UPDATE_SUBSCRIPTION"
WEBSOCKET_ACTION_UPDATE_CARD_LIMIT_TIMESTAMP = "UPDATE_CARD_LIMIT_TIMESTAMP"
WEBSOCKET_ACTION_REORDER_CATEGORIES = "REORDER_CATEGORIES"
WEBSOCKET_ACTION_REORDER_CATEGORY_BOARDS = "REORDER_CATEGORY_BOARDS"

# List to store active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


# Pydantic models
class Block(BaseModel):
    block_id: str
    content: Optional[str] = None


class BoardMember(BaseModel):
    user_id: str
    board_id: str


class ClientConfig(BaseModel):
    config_name: str
    config_value: str


class Category(BaseModel):
    category_id: str
    category_name: str


class BoardCategoryWebsocketData(BaseModel):
    board_id: str
    category_id: str


class Subscription(BaseModel):
    subscription_id: str
    team_id: str


# Store class equivalent in Python
class Store:
    async def get_block(self, block_id: str) -> Optional[Block]:
        """
        Retrieve a block by its ID.
        :param block_id: ID of the block
        :return: Block object or None
        """
        # Implement logic to fetch block
        return Block(block_id=block_id, content="Example content")

    async def get_members_for_board(self, board_id: str) -> List[BoardMember]:
        """
        Retrieve all members for a specific board.
        :param board_id: ID of the board
        :return: List of BoardMember objects
        """
        # Implement logic to fetch members for the board
        return [BoardMember(user_id="user1", board_id=board_id)]


# Adapter class with broadcasting logic
class Adapter:
    async def broadcast_block_change(self, team_id: str, block: Block):
        """
        Broadcast block change to all connected clients.
        :param team_id: ID of the team
        :param block: Block object with updated data
        """
        await manager.broadcast(f"Block {block.block_id} changed for team {team_id}")

    async def broadcast_block_delete(self, team_id: str, block_id: str, board_id: str):
        """
        Broadcast block deletion event to all connected clients.
        :param team_id: ID of the team
        :param block_id: ID of the block
        :param board_id: ID of the board the block belonged to
        """
        await manager.broadcast(f"Block {block_id} deleted for team {team_id} on board {board_id}")

    async def broadcast_board_change(self, team_id: str, board_id: str):
        """
        Broadcast board change event to all connected clients.
        :param team_id: ID of the team
        :param board_id: ID of the updated board
        """
        await manager.broadcast(f"Board {board_id} changed for team {team_id}")

    async def broadcast_board_delete(self, team_id: str, board_id: str):
        """
        Broadcast board deletion event to all connected clients.
        :param team_id: ID of the team
        :param board_id: ID of the board to delete
        """
        await manager.broadcast(f"Board {board_id} deleted for team {team_id}")

    async def broadcast_member_change(self, team_id: str, board_id: str, member: BoardMember):
        """
        Broadcast member change event to all connected clients.
        :param team_id: ID of the team
        :param board_id: ID of the board
        :param member: Updated BoardMember object
        """
        await manager.broadcast(f"Member {member.user_id} updated for board {board_id} in team {team_id}")

    async def broadcast_member_delete(self, team_id: str, board_id: str, user_id: str):
        """
        Broadcast member deletion event to all connected clients.
        :param team_id: ID of the team
        :param board_id: ID of the board
        :param user_id: ID of the user to delete
        """
        await manager.broadcast(f"Member {user_id} deleted from board {board_id} in team {team_id}")

    async def broadcast_config_change(self, client_config: ClientConfig):
        """
        Broadcast configuration change event to all connected clients.
        :param client_config: Updated ClientConfig object
        """
        await manager.broadcast(f"Client config {client_config.config_name} changed")

    async def broadcast_category_change(self, category: Category):
        """
        Broadcast category change event to all connected clients.
        :param category: Updated Category object
        """
        await manager.broadcast(f"Category {category.category_name} updated")

    async def broadcast_category_board_change(self, team_id: str, user_id: str, block_category: List[BoardCategoryWebsocketData]):
        """
        Broadcast category board change event to all connected clients.
        :param team_id: ID of the team
        :param user_id: ID of the user
        :param block_category: List of updated BoardCategoryWebsocketData
        """
        await manager.broadcast(f"Category board updated by user {user_id} in team {team_id}")

    async def broadcast_card_limit_timestamp_change(self, card_limit_timestamp: int):
        """
        Broadcast card limit timestamp change event to all connected clients.
        :param card_limit_timestamp: New card limit timestamp
        """
        await manager.broadcast(f"Card limit timestamp updated to {card_limit_timestamp}")

    async def broadcast_subscription_change(self, team_id: str, subscription: Subscription):
        """
        Broadcast subscription change event to all connected clients.
        :param team_id: ID of the team
        :param subscription: Updated Subscription object
        """
        await manager.broadcast(f"Subscription {subscription.subscription_id} changed for team {team_id}")

    async def broadcast_category_reorder(self, team_id: str, user_id: str, category_order: List[str]):
        """
        Broadcast category reorder event to all connected clients.
        :param team_id: ID of the team
        :param user_id: ID of the user
        :param category_order: List of reordered category IDs
        """
        await manager.broadcast(f"Categories reordered by user {user_id} in team {team_id}")

    async def broadcast_category_boards_reorder(self, team_id: str, user_id: str, category_id: str, boards_order: List[str]):
        """
        Broadcast category boards reorder event to all connected clients.
        :param team_id: ID of the team
        :param user_id: ID of the user
        :param category_id: ID of the category
        :param boards_order: List of reordered board IDs
        """
        await manager.broadcast(f"Boards reordered in category {category_id} by user {user_id} in team {team_id}")


# WebSocket route for communication
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # You can add logic to handle WebSocket messages here
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
