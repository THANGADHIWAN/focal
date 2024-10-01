from fastapi import FastAPI, HTTPException, Depends, Path, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Define models
class Card(BaseModel):
    id: str
    board_id: str
    title: str
    description: Optional[str] = None

class CardPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ErrorResponse(BaseModel):
    message: str

# Sample in-memory storage
cards_db = {}
permissions = {
    "user_id": "user_permission"  # Sample permission structure
}

# Dependency to check permissions
def check_permissions(user_id: str, board_id: str, permission: str):
    if permissions.get(user_id) != permission:
        raise HTTPException(status_code=403, detail="Access denied")

# Route to create a card
@app.post("/boards/{board_id}/cards", response_model=Card)
async def create_card(
    board_id: str,
    card: Card,
    disable_notify: Optional[bool] = Query(False),
    user_id: str = Depends(lambda: "user_id")  # Mocking user ID retrieval
):
    check_permissions(user_id, board_id, "manage_cards")
    if card.board_id != board_id:
        raise HTTPException(status_code=400, detail="Board ID mismatch")
    
    card.id = str(len(cards_db) + 1)  # Simple ID generation
    cards_db[card.id] = card
    return card

# Route to get cards
@app.get("/boards/{board_id}/cards", response_model=List[Card])
async def get_cards(
    board_id: str,
    page: int = Query(0),
    per_page: int = Query(100),
    user_id: str = Depends(lambda: "user_id")
):
    check_permissions(user_id, board_id, "view_board")
    cards = [card for card in cards_db.values() if card.board_id == board_id]
    return cards[page * per_page: (page + 1) * per_page]

# Route to patch a card
@app.patch("/cards/{card_id}", response_model=Card)
async def patch_card(
    card_id: str,
    card_patch: CardPatch,
    disable_notify: Optional[bool] = Query(False),
    user_id: str = Depends(lambda: "user_id")
):
    card = cards_db.get(card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    check_permissions(user_id, card.board_id, "manage_cards")

    if card_patch.title:
        card.title = card_patch.title
    if card_patch.description:
        card.description = card_patch.description
    
    return card

# Route to get a specific card
@app.get("/cards/{card_id}", response_model=Card)
async def get_card(card_id: str, user_id: str = Depends(lambda: "user_id")):
    card = cards_db.get(card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    check_permissions(user_id, card.board_id, "manage_cards")
    return card
