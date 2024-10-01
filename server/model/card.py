from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conlist, Field
from typing import Any, Dict, List, Optional
import time

app = FastAPI()

# Error definitions
class CardError(Exception):
    pass

class ErrInvalidCard(CardError):
    def __init__(self, msg: str):
        super().__init__(f"Invalid card: {msg}")

class ErrNotCardBlock(CardError):
    pass

class ErrInvalidFieldType(CardError):
    def __init__(self, field: str):
        super().__init__(f"Invalid type for field '{field}'")

# Data models
class Card(BaseModel):
    id: str = Field(default_factory=lambda: utils.new_id('card'))
    board_id: str
    created_by: str
    modified_by: str
    title: str
    content_order: List[str] = []
    icon: str
    is_template: bool
    properties: Dict[str, Any] = {}
    create_at: int = Field(default_factory=lambda: int(time.time() * 1000))
    update_at: int = Field(default_factory=lambda: int(time.time() * 1000))
    delete_at: Optional[int] = None

    def check_valid(self):
        if not self.id:
            raise ErrInvalidCard("ID is missing")
        if not self.board_id:
            raise ErrInvalidCard("BoardID is missing")
        if not self.content_order:
            raise ErrInvalidCard("ContentOrder is missing")
        if len(self.icon) > 1:
            raise ErrInvalidCard("Icon can have only one grapheme")
        if not self.properties:
            raise ErrInvalidCard("Properties are missing")
        if self.create_at == 0:
            raise ErrInvalidCard("CreateAt is missing")
        if self.update_at == 0:
            raise ErrInvalidCard("UpdateAt is missing")

class CardPatch(BaseModel):
    title: Optional[str]
    content_order: Optional[List[str]]
    icon: Optional[str]
    updated_properties: Dict[str, Any] = {}

    def check_valid(self):
        if self.icon and len(self.icon) > 1:
            raise ErrInvalidCard("Icon can have only one grapheme")

# Utility functions
def card_to_block(card: Card):
    return {
        "id": card.id,
        "parent_id": card.board_id,
        "created_by": card.created_by,
        "modified_by": card.modified_by,
        "title": card.title,
        "fields": {
            "content_order": card.content_order,
            "icon": card.icon,
            "is_template": card.is_template,
            "properties": card.properties,
        },
        "create_at": card.create_at,
        "update_at": card.update_at,
        "delete_at": card.delete_at,
    }

def block_to_card(block: dict) -> Card:
    if block.get("type") != "card":
        raise ErrNotCardBlock("Cannot convert block to card")
    
    return Card(
        id=block["id"],
        board_id=block["parent_id"],
        created_by=block["created_by"],
        modified_by=block["modified_by"],
        title=block["title"],
        content_order=block["fields"].get("content_order", []),
        icon=block["fields"].get("icon", ""),
        is_template=block["fields"].get("is_template", False),
        properties=block["fields"].get("properties", {}),
        create_at=block["create_at"],
        update_at=block["update_at"],
        delete_at=block.get("delete_at"),
    )

# Endpoints
@app.post("/cards/", response_model=Card)
async def create_card(card: Card):
    card.check_valid()
    # Here you would typically save the card to a database
    return card

@app.patch("/cards/{card_id}", response_model=Card)
async def update_card(card_id: str, patch: CardPatch):
    # Here you would typically retrieve the card from a database
    # Simulated card for example purposes
    card = Card(id=card_id, board_id="example", created_by="user", modified_by="user", title="Example Card")
    
    patch.check_valid()
    if patch.title is not None:
        card.title = patch.title
    if patch.content_order is not None:
        card.content_order = patch.content_order
    if patch.icon is not None:
        card.icon = patch.icon
    card.properties.update(patch.updated_properties)
    card.update_at = int(time.time() * 1000)  # Update the timestamp
    
    return card

@app.get("/cards/{card_id}", response_model=Card)
async def get_card(card_id: str):
    # Simulated card retrieval
    card = Card(id=card_id, board_id="example", created_by="user", modified_by="user", title="Example Card")
    return card

# Run the application
# Use 'uvicorn filename:app --reload' to run the app
