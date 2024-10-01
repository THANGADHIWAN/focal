from fastapi import FastAPI, WebSocket
from typing import List, Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New connection: {websocket}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Disconnected: {websocket}")

    async def broadcast(self, message: Dict[str, Any]):
        for connection in self.active_connections:
            await connection.send_json(message)
            logger.info(f"Broadcast message: {message} to {connection}")

class WSAdapter:
    def __init__(self, app: FastAPI):
        self.app = app
        self.manager = WebSocketManager()
        self.setup_routes()

    def setup_routes(self):
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await self.manager.connect(websocket)
            try:
                while True:
                    data = await websocket.receive_json()
                    # Process the received data
                    logger.info(f"Received data: {data}")
                    await self.manager.broadcast({"message": "You sent: " + data.get("message", "")})
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
            finally:
                self.manager.disconnect(websocket)

# Create FastAPI app
app = FastAPI()
ws_adapter = WSAdapter(app)

# To run the application, use the command: uvicorn <filename>:app --reload
