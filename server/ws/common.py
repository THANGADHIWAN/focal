from pydantic import BaseModel
from typing import List, Optional
from fastapi import WebSocket

# Model for Category
class Category(BaseModel):
    category_id: str
    category_name: str

# Model for BoardCategoryWebsocketData
class BoardCategoryWebsocketData(BaseModel):
    block_id: str
    board_id: str

# UpdateCategoryMessage is sent on category updates
class UpdateCategoryMessage(BaseModel):
    action: str
    team_id: str
    category: Optional[Category] = None
    block_categories: Optional[List[BoardCategoryWebsocketData]] = None

# Model for Block
class Block(BaseModel):
    block_id: str
    content: Optional[str] = None

# UpdateBlockMsg is sent on block updates
class UpdateBlockMsg(BaseModel):
    action: str
    team_id: str
    block: Block

# Model for Board
class Board(BaseModel):
    board_id: str
    board_name: str

# UpdateBoardMsg is sent on board updates
class UpdateBoardMsg(BaseModel):
    action: str
    team_id: str
    board: Board

# Model for BoardMember
class BoardMember(BaseModel):
    user_id: str
    board_id: str

# UpdateMemberMsg is sent on membership updates
class UpdateMemberMsg(BaseModel):
    action: str
    team_id: str
    member: BoardMember

# Model for Subscription
class Subscription(BaseModel):
    subscription_id: str
    team_id: str

# UpdateSubscription is sent on subscription updates
class UpdateSubscription(BaseModel):
    action: str
    subscription: Subscription

# Model for ClientConfig
class ClientConfig(BaseModel):
    config_name: str
    config_value: str

# UpdateClientConfig is sent on client config updates
class UpdateClientConfig(BaseModel):
    action: str
    clientconfig: ClientConfig

# UpdateCardLimitTimestamp is sent on card limit timestamp updates
class UpdateCardLimitTimestamp(BaseModel):
    action: str
    timestamp: int

# WebsocketCommand is an incoming command from the client
class WebsocketCommand(BaseModel):
    action: str
    team_id: str
    token: str
    read_token: str
    block_ids: Optional[List[str]] = None

# CategoryReorderMessage is sent when categories are reordered
class CategoryReorderMessage(BaseModel):
    action: str
    category_order: List[str]
    team_id: str

# CategoryBoardReorderMessage is sent when boards in a category are reordered
class CategoryBoardReorderMessage(BaseModel):
    action: str
    category_id: str
    board_order: List[str]
    team_id: str


# Example WebSocket handler using FastAPI
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming WebSocket data here, e.g., parsing `WebsocketCommand`
            # Here you can receive and process commands, and then broadcast messages.
            await manager.broadcast(f"Message received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
