from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# Data model for BoardsCloudLimits
class BoardsCloudLimits(BaseModel):
    cards: int = Field(..., title="The maximum number of cards on the server")
    used_cards: int = Field(..., alias="used_cards", title="The current number of cards on the server")
    card_limit_timestamp: int = Field(..., title="The updated_at timestamp of the limit card")
    views: int = Field(..., title="The maximum number of views for each board")

# Example in-memory data storage
limits_data = BoardsCloudLimits(
    cards=1000,
    used_cards=500,
    card_limit_timestamp=1633094400,  # Example timestamp
    views=100
)

# Endpoint to get the board limits
@app.get("/boards_limits", response_model=BoardsCloudLimits)
async def get_boards_limits():
    return limits_data

# Endpoint to update the board limits
@app.post("/boards_limits", response_model=BoardsCloudLimits)
async def update_boards_limits(limits: BoardsCloudLimits):
    global limits_data
    limits_data = limits
    return limits_data

# Run the application
# Use 'uvicorn filename:app --reload' to run the app
