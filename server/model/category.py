from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, constr
from typing import Optional
import time

app = FastAPI()

# Constants
CATEGORY_TYPE_SYSTEM = "system"
CATEGORY_TYPE_CUSTOM = "custom"

# Data models
class Category(BaseModel):
    id: str = Field(..., title="The id for this category")
    name: str = Field(..., title="The name for this category")
    user_id: str = Field(..., title="The user's id for this category")
    team_id: str = Field(..., title="The team id for this category")
    create_at: int = Field(..., title="The creation time in milliseconds since the current epoch")
    update_at: int = Field(..., title="The last modified time in milliseconds since the current epoch")
    delete_at: Optional[int] = Field(None, title="The deleted time in milliseconds since the current epoch")
    collapsed: bool = Field(..., title="Category's state on client side")
    sort_order: int = Field(..., title="Inter-category sort order per user")
    sorting: str = Field(..., title="The sorting method applied on this category")
    type: constr(regex="^(system|custom)$") = Field(..., title="Category's type")

    def hydrate(self):
        if not self.id:
            self.id = utils_new_id()  # Placeholder for ID generation

        if self.create_at == 0:
            self.create_at = int(time.time() * 1000)

        if self.update_at == 0:
            self.update_at = self.create_at

        if self.sort_order < 0:
            self.sort_order = 0

        if not self.type.strip():
            self.type = CATEGORY_TYPE_CUSTOM

    def is_valid(self):
        if not self.id.strip():
            raise ValueError("Category ID cannot be empty")
        if not self.name.strip():
            raise ValueError("Category name cannot be empty")
        if not self.user_id.strip():
            raise ValueError("Category user ID cannot be empty")
        if not self.team_id.strip():
            raise ValueError("Category team ID cannot be empty")
        if self.type not in (CATEGORY_TYPE_CUSTOM, CATEGORY_TYPE_SYSTEM):
            raise ValueError(f"Invalid category type. Allowed types: {CATEGORY_TYPE_SYSTEM} and {CATEGORY_TYPE_CUSTOM}")

# Example in-memory data storage
categories = {}

# Utility functions
def utils_new_id():
    return str(int(time.time() * 1000))  # Placeholder for a unique ID generator

# Endpoints
@app.post("/categories/", response_model=Category)
async def create_category(category: Category):
    category.hydrate()
    category.is_valid()

    if category.id in categories:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    categories[category.id] = category
    return category

@app.get("/categories/{category_id}", response_model=Category)
async def get_category(category_id: str):
    if category_id not in categories:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return categories[category_id]

@app.patch("/categories/{category_id}", response_model=Category)
async def update_category(category_id: str, category: Category):
    if category_id not in categories:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category.hydrate()  # Update timestamps
    category.is_valid()
    categories[category_id] = category
    return category

@app.delete("/categories/{category_id}")
async def delete_category(category_id: str):
    if category_id not in categories:
        raise HTTPException(status_code=404, detail="Category not found")
    
    del categories[category_id]
    return {"detail": "Category deleted"}

# Run the application
# Use 'uvicorn filename:app --reload' to run the app
