from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Define the data models
class Block(BaseModel):
    id: str
    content: str

class BoardMember(BaseModel):
    user_id: str
    board_id: str
    role: str

# Create a mock store class
class Store:
    def get_block(self, block_id: str) -> Optional[Block]:
        raise NotImplementedError

    def get_members_for_board(self, board_id: str) -> List[BoardMember]:
        raise NotImplementedError

class MockStore(Store):
    def __init__(self):
        self.blocks = {}
        self.members = {}

    def get_block(self, block_id: str) -> Optional[Block]:
        return self.blocks.get(block_id, None)

    def get_members_for_board(self, board_id: str) -> List[BoardMember]:
        return self.members.get(board_id, [])

# Initialize FastAPI app and store
app = FastAPI()
store = MockStore()

@app.get("/block/{block_id}", response_model=Block)
async def get_block(block_id: str):
    block = store.get_block(block_id)
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    return block

@app.get("/board/{board_id}/members", response_model=List[BoardMember])
async def get_members_for_board(board_id: str):
    members = store.get_members_for_board(board_id)
    return members

# Example route to populate mock data (for demonstration purposes)
@app.post("/mock_data")
async def add_mock_data():
    # Add a sample block
    store.blocks["block1"] = Block(id="block1", content="Sample Block Content")
    # Add members for a board
    store.members["board1"] = [
        BoardMember(user_id="user1", board_id="board1", role="admin"),
        BoardMember(user_id="user2", board_id="board1", role="member"),
    ]
    return {"message": "Mock data added"}

# Entry point for running the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
