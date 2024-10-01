from fastapi import FastAPI, HTTPException, Depends, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import logging

app = FastAPI()

# Set up logging
logger = logging.getLogger("api")
logging.basicConfig(level=logging.DEBUG)

# Sample data models
class Board(BaseModel):
    id: str
    type: str

class ErrorResponse(BaseModel):
    error: str

# Sample in-memory data for demonstration
boards_data = []  # Replace with actual data fetching logic

# Dummy function to simulate fetching the user ID from a session
def get_user_id():
    return "user-123"

# Dummy function to simulate permission checking
def has_permission_to_team(user_id: str, team_id: str, permission: str) -> bool:
    return True  # Implement actual permission logic

def user_is_guest(user_id: str) -> bool:
    return False  # Implement actual guest checking logic

@app.get("/teams/{team_id}/templates", response_model=List[Board], responses={404: {"model": ErrorResponse}})
async def handle_get_templates(team_id: str, user_id: str = Depends(get_user_id)):
    """Returns team templates"""
    
    # Check permissions
    if team_id != "global_team_id" and not has_permission_to_team(user_id, team_id, "view"):
        raise HTTPException(status_code=403, detail="Access denied to team")

    if user_is_guest(user_id):
        raise HTTPException(status_code=403, detail="Access denied to templates")

    # Audit logging
    logger.info(f"Getting templates for team_id: {team_id}")

    # Retrieve boards list (replace with actual fetching logic)
    boards = [board for board in boards_data if board['team_id'] == team_id]

    results = []
    for board in boards:
        if board['type'] == "open":
            results.append(board)
        elif has_permission_to_team(user_id, board['id'], "view"):
            results.append(board)

    logger.debug(f"GetTemplates - teamID: {team_id}, boardsCount: {len(results)}")

    if not results:
        raise HTTPException(status_code=404, detail="No templates found")

    return results
