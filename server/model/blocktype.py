from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Union, Dict, Any

app = FastAPI()

# BlockType enumeration
class BlockType(str):
    UNKNOWN = "unknown"
    BOARD = "board"
    CARD = "card"
    VIEW = "view"
    TEXT = "text"
    CHECKBOX = "checkbox"
    COMMENT = "comment"
    IMAGE = "image"
    ATTACHMENT = "attachment"
    DIVIDER = "divider"

    @classmethod
    def from_string(cls, s: str) -> 'BlockType':
        """Returns appropriate BlockType for the specified string."""
        s = s.lower()
        if s in cls.__dict__.values():
            return BlockType(s)
        raise InvalidBlockTypeError(s)

class InvalidBlockTypeError(Exception):
    """Exception for invalid block type."""
    def __init__(self, block_type: str):
        self.block_type = block_type
        super().__init__(f"{block_type} is an invalid block type.")

# Utility function to map BlockType to IDType
def block_type_to_id_type(block_type: BlockType) -> str:
    """Returns appropriate IDType for the specified BlockType."""
    if block_type == BlockType.BOARD:
        return "IDTypeBoard"
    elif block_type == BlockType.CARD:
        return "IDTypeCard"
    elif block_type == BlockType.VIEW:
        return "IDTypeView"
    elif block_type in {BlockType.TEXT, BlockType.CHECKBOX, BlockType.COMMENT, BlockType.DIVIDER}:
        return "IDTypeBlock"
    elif block_type in {BlockType.IMAGE, BlockType.ATTACHMENT}:
        return "IDTypeAttachment"
    return "IDTypeNone"

# Endpoint to convert string to BlockType
@app.get("/block-type/", response_model=str)
def get_block_type(type_str: str):
    try:
        block_type = BlockType.from_string(type_str)
        return block_type
    except InvalidBlockTypeError as e:
        raise HTTPException(status_code=400, detail=str(e))

# To run the FastAPI app: uvicorn main:app --reload
