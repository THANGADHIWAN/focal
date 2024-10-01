from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# Allow CORS for all origins (modify as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Category(BaseModel):
    id: str
    user_id: str
    team_id: str
    name: str

class CategoryBoards(BaseModel):
    category_id: str
    boards: List[str]

# Mock data store
categories = {}
user_permissions = {}

# Dependency for session retrieval
async def get_current_user():
    # Mock session retrieval
    return {"user_id": "current_user_id"}

@app.post("/teams/{team_id}/categories", response_model=Category)
async def create_category(team_id: str, category: Category, current_user: Dict = Depends(get_current_user)):
    if category.user_id != current_user['user_id']:
        raise HTTPException(status_code=400, detail="User ID mismatch")
    
    if category.team_id != team_id:
        raise HTTPException(status_code=400, detail="Team ID mismatch")

    # Check permissions
    if not user_permissions.get(current_user['user_id'], {}).get(team_id, False):
        raise HTTPException(status_code=403, detail="Access denied to team")

    categories[category.id] = category
    return category

@app.put("/teams/{team_id}/categories/{category_id}", response_model=Category)
async def update_category(team_id: str, category_id: str, category: Category, current_user: Dict = Depends(get_current_user)):
    if category.id != category_id:
        raise HTTPException(status_code=400, detail="Category ID mismatch")
    
    if category.user_id != current_user['user_id']:
        raise HTTPException(status_code=400, detail="User ID mismatch")
    
    if category.team_id != team_id:
        raise HTTPException(status_code=400, detail="Team ID mismatch")

    if category_id not in categories:
        raise HTTPException(status_code=404, detail="Category not found")

    categories[category_id] = category
    return category

@app.delete("/teams/{team_id}/categories/{category_id}")
async def delete_category(team_id: str, category_id: str, current_user: Dict = Depends(get_current_user)):
    if category_id not in categories:
        raise HTTPException(status_code=404, detail="Category not found")

    if not user_permissions.get(current_user['user_id'], {}).get(team_id, False):
        raise HTTPException(status_code=403, detail="Access denied to team")

    del categories[category_id]
    return {"detail": "Category deleted"}

@app.get("/teams/{team_id}/categories", response_model=List[Category])
async def get_user_category_boards(team_id: str, current_user: Dict = Depends(get_current_user)):
    if not user_permissions.get(current_user['user_id'], {}).get(team_id, False):
        raise HTTPException(status_code=403, detail="Access denied to team")

    user_categories = [cat for cat in categories.values() if cat.team_id == team_id and cat.user_id == current_user['user_id']]
    return user_categories

@app.put("/teams/{team_id}/categories/reorder")
async def reorder_categories(team_id: str, new_order: List[str], current_user: Dict = Depends(get_current_user)):
    if not user_permissions.get(current_user['user_id'], {}).get(team_id, False):
        raise HTTPException(status_code=403, detail="Access denied to team")

    # Update the order (mock behavior)
    # Assuming new_order is a list of category IDs
    return {"detail": "Categories reordered"}

# Additional routes would be added here in a similar manner.

# To run the application, use:
# uvicorn your_filename:app --reload
