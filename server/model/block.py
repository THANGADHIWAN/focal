from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, constr, conint
from typing import Optional, List, Dict, Any
import json
from datetime import datetime

app = FastAPI()

# Constants
BLOCK_TITLE_MAX_BYTES = 65535
BLOCK_TITLE_MAX_RUNES = BLOCK_TITLE_MAX_BYTES // 4
BLOCK_FIELDS_MAX_RUNES = 800000

class Block(BaseModel):
    id: str
    parent_id: Optional[str] = None
    created_by: str
    modified_by: str
    schema: int
    type: str  # Use Enum for BlockType if needed
    title: Optional[constr(max_length=BLOCK_TITLE_MAX_RUNES)] = None
    fields: Optional[Dict[str, Any]] = Field(default_factory=dict)
    create_at: conint(ge=0)
    update_at: conint(ge=0)
    delete_at: Optional[int] = None
    board_id: str
    limited: Optional[bool] = False

    def is_valid(self):
        if not self.board_id:
            raise HTTPException(status_code=400, detail="boardID is empty")
        
        if len(self.title.encode('utf-8')) > BLOCK_TITLE_MAX_BYTES:
            raise HTTPException(status_code=400, detail="block title size limit exceeded")

        fields_json = json.dumps(self.fields)
        if len(fields_json.encode('utf-8')) > BLOCK_FIELDS_MAX_RUNES:
            raise HTTPException(status_code=400, detail="block fields size limit exceeded")

class BlockPatch(BaseModel):
    parent_id: Optional[str] = None
    schema: Optional[int] = None
    type: Optional[str] = None
    title: Optional[str] = None
    updated_fields: Optional[Dict[str, Any]] = Field(default_factory=dict)
    deleted_fields: Optional[List[str]] = Field(default_factory=list)

class BlockPatchBatch(BaseModel):
    block_ids: List[str]
    block_patches: List[BlockPatch]

@app.post("/blocks/", response_model=Block)
def create_block(block: Block):
    block.is_valid()
    block.create_at = int(datetime.now().timestamp() * 1000)
    block.update_at = block.create_at
    # In a real app, save to DB here
    return block

@app.patch("/blocks/{block_id}", response_model=Block)
def patch_block(block_id: str, patch: BlockPatch):
    # Retrieve block from DB (mocked)
    block = Block(id=block_id, created_by="user", modified_by="user", schema=1, type="type", create_at=int(datetime.now().timestamp() * 1000), update_at=int(datetime.now().timestamp() * 1000), board_id="board_id")
    # Apply patch logic
    if patch.parent_id is not None:
        block.parent_id = patch.parent_id
    if patch.schema is not None:
        block.schema = patch.schema
    if patch.type is not None:
        block.type = patch.type
    if patch.title is not None:
        block.title = patch.title
    for key, value in patch.updated_fields.items():
        block.fields[key] = value
    for key in patch.deleted_fields:
        if key in block.fields:
            del block.fields[key]
    block.update_at = int(datetime.now().timestamp() * 1000)
    # In a real app, save to DB here
    return block

@app.get("/blocks/{block_id}", response_model=Block)
def get_block(block_id: str):
    # Mock retrieval
    block = Block(id=block_id, created_by="user", modified_by="user", schema=1, type="type", create_at=int(datetime.now().timestamp() * 1000), update_at=int(datetime.now().timestamp() * 1000), board_id="board_id")
    return block

# For running the FastAPI server, use: uvicorn main:app --reload
