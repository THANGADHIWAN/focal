from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import json

app = FastAPI()

# Define the Sharing model using Pydantic
class Sharing(BaseModel):
    id: str
    enabled: bool
    token: str
    modified_by: str  # Renamed to follow Python naming conventions
    update_at: Optional[int] = None  # Optional field

# Function to create Sharing object from JSON (similar to SharingFromJSON)
def sharing_from_json(data: str) -> Sharing:
    return Sharing.parse_raw(data)

# Example route to create a Sharing object from JSON
@app.post("/sharing/", response_model=Sharing)
async def create_sharing(sharing: Sharing):
    return sharing

# Example route to parse JSON string into a Sharing object
@app.post("/sharing/parse/")
async def parse_sharing(json_data: str):
    try:
        sharing = sharing_from_json(json_data)
        return sharing
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")

# To run the FastAPI server, use:
# uvicorn filename:app --reload
