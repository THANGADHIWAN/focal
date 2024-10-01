from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conlist
from typing import List, Optional

app = FastAPI()

# Error definitions
class BoardError(Exception):
    pass

class NoBoardsError(BoardError):
    def __str__(self):
        return "At least one board is required."

class NoBlocksError(BoardError):
    def __str__(self):
        return "At least one block is required."

class BlockDoesntBelongToAnyBoardError(BoardError):
    def __init__(self, block_id: str):
        self.block_id = block_id

    def __str__(self):
        return f"Block {self.block_id} doesn't belong to any board."


# Data models
class Block(BaseModel):
    id: str
    board_id: str
    type: str

class Board(BaseModel):
    id: str
    title: str
    type: str

class BoardsAndBlocks(BaseModel):
    boards: List[Board]
    blocks: List[Block]

    def validate(self):
        if not self.boards:
            raise NoBoardsError()
        if not self.blocks:
            raise NoBlocksError()
        
        board_ids = {board.id for board in self.boards}
        for block in self.blocks:
            if block.board_id not in board_ids:
                raise BlockDoesntBelongToAnyBoardError(block.id)


class DeleteBoardsAndBlocks(BaseModel):
    boards: List[str]
    blocks: List[str]

    def validate(self):
        if not self.boards:
            raise NoBoardsError()
        if not self.blocks:
            raise NoBlocksError()


class PatchBoard(BaseModel):
    title: Optional[str]
    description: Optional[str]

class PatchBoardsAndBlocks(BaseModel):
    board_ids: List[str]
    board_patches: List[PatchBoard]
    block_ids: List[str]
    block_patches: List[PatchBoard]

    def validate(self):
        if not self.board_ids:
            raise NoBoardsError()
        if len(self.board_ids) != len(self.board_patches):
            raise HTTPException(status_code=400, detail="Board IDs and patches need to match.")
        if len(self.block_ids) != len(self.block_patches):
            raise HTTPException(status_code=400, detail="Block IDs and patches need to match.")

# Endpoints
@app.post("/boards_and_blocks/")
async def create_boards_and_blocks(bab: BoardsAndBlocks):
    try:
        bab.validate()
        # Logic for generating new IDs can go here
        return bab
    except BoardError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete_boards_and_blocks/")
async def delete_boards_and_blocks(dbab: DeleteBoardsAndBlocks):
    try:
        dbab.validate()
        return dbab
    except BoardError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.patch("/patch_boards_and_blocks/")
async def patch_boards_and_blocks(pbab: PatchBoardsAndBlocks):
    try:
        pbab.validate()
        return pbab
    except BoardError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Run the application
# Use 'uvicorn filename:app --reload' to run the app
