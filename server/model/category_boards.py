from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

# Constants
CATEGORY_BOARDS_SORT_ORDER_GAP = 10

# Data models
class Category(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

class CategoryBoardMetadata(BaseModel):
    board_id: str
    hidden: bool

class CategoryBoards(Category):
    board_metadata: List[CategoryBoardMetadata] = Field(..., title="The IDs of boards in this category")
    sort_order: int = Field(..., title="The relative sort order of this board in its category")

class BoardCategoryWebsocketData(BaseModel):
    board_id: str
    category_id: str
    hidden: bool

# Example in-memory data storage
categories = {}

# Endpoints
@app.post("/categories/", response_model=CategoryBoards)
async def create_category_boards(category_boards: CategoryBoards):
    if category_boards.id in categories:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    categories[category_boards.id] = category_boards
    return category_boards

@app.get("/categories/{category_id}", response_model=CategoryBoards)
async def get_category_boards(category_id: str):
    if category_id not in categories:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return categories[category_id]

@app.patch("/categories/{category_id}", response_model=CategoryBoards)
async def update_category_boards(category_id: str, category_boards: CategoryBoards):
    if category_id not in categories:
        raise HTTPException(status_code=404, detail="Category not found")
    
    categories[category_id] = category_boards
    return category_boards

@app.delete("/categories/{category_id}")
async def delete_category_boards(category_id: str):
    if category_id not in categories:
        raise HTTPException(status_code=404, detail="Category not found")
    
    del categories[category_id]
    return {"detail": "Category deleted"}

# Run the application
# Use 'uvicorn filename:app --reload' to run the app
