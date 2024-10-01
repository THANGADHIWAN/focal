from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, constr
from typing import List, Dict, Any, Optional
import uuid
import logging

app = FastAPI()

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def new_id(block_type: str) -> str:
    """Generates a new unique ID based on block type."""
    return str(uuid.uuid4())

# Pydantic models
class Block(BaseModel):
    id: str
    parent_id: Optional[str] = None
    board_id: str
    type: str
    fields: Dict[str, Any]

class BlockIDGenerator:
    def __init__(self):
        self.block_ids = {}
        self.reference_ids = {}

    def generate_ids(self, blocks: List[Block]) -> List[Block]:
        # Track unique block IDs and references
        for block in blocks:
            self.block_ids[block.id] = block.type
            self.reference_ids[block.board_id] = True
            if block.parent_id:
                self.reference_ids[block.parent_id] = True
            
            # Handle contentOrder and defaultTemplateId fields
            self._track_references(block)

        new_ids = {id: new_id(block_type) for id, block_type in self.block_ids.items()}

        # Update blocks with new IDs
        for block in blocks:
            block.id = self._get_existing_or_new_id(block.id, new_ids)
            block.board_id = self._get_existing_or_old_id(block.board_id, new_ids)
            block.parent_id = self._get_existing_or_old_id(block.parent_id, new_ids)
            self._fix_field_ids(block, "contentOrder", new_ids)
            self._fix_field_ids(block, "cardOrder", new_ids)
            if "defaultTemplateId" in block.fields:
                default_template_id = block.fields["defaultTemplateId"]
                block.fields["defaultTemplateId"] = self._get_existing_or_old_id(default_template_id, new_ids)

        return blocks

    def _track_references(self, block: Block):
        """Track references for fields that contain block IDs."""
        if "contentOrder" in block.fields:
            content_order = block.fields["contentOrder"]
            if isinstance(content_order, list):
                for block_id in content_order:
                    if isinstance(block_id, str):
                        self.reference_ids[block_id] = True

        if "defaultTemplateId" in block.fields:
            default_template_id = block.fields["defaultTemplateId"]
            if isinstance(default_template_id, str):
                self.reference_ids[default_template_id] = True

    def _get_existing_or_old_id(self, id: str, new_ids: Dict[str, str]) -> str:
        return new_ids.get(id, id)

    def _get_existing_or_new_id(self, id: str, new_ids: Dict[str, str]) -> str:
        return new_ids.get(id, new_id(self.block_ids[id]))

    def _fix_field_ids(self, block: Block, field_name: str, new_ids: Dict[str, str]):
        if field_name in block.fields and isinstance(block.fields[field_name], list):
            field = block.fields[field_name]
            for i in range(len(field)):
                if isinstance(field[i], str):
                    field[i] = self._get_existing_or_old_id(field[i], new_ids)

# Endpoint to generate block IDs
@app.post("/generate-block-ids/", response_model=List[Block])
def generate_block_ids(blocks: List[Block]):
    generator = BlockIDGenerator()
    return generator.generate_ids(blocks)

# To run the FastAPI app: uvicorn main:app --reload
