from fastapi import FastAPI, HTTPException, Depends, Path, Query
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
class User(BaseModel):
    id: str
    username: str
    email: str
    create_at: int
    update_at: int
    permissions: List[str] = []

class UserPreferencesPatch(BaseModel):
    # Define the user preferences fields that can be patched
    pass

class ErrorResponse(BaseModel):
    error: str

# Dummy functions to simulate data fetching and permission checking
def get_user_id():
    return "user-123"  # Simulate user ID retrieval

def has_permission_to(user_id: str, permission: str) -> bool:
    return True  # Simulate permission checking

def can_see_user(current_user_id: str, target_user_id: str) -> bool:
    return True  # Simulate user visibility check

# Sample in-memory data for demonstration
users_data = []  # Replace with actual data fetching logic

@app.post("/users", response_model=List[User], responses={400: {"model": ErrorResponse}})
async def handle_get_users_list(user_ids: List[str]):
    """Returns a list of users based on provided user IDs"""
    if not user_ids:
        raise HTTPException(status_code=400, detail="User IDs are empty")

    users = []
    for user_id in user_ids:
        if user_id == "single_user":
            user = User(id="single_user", username="single_user", email="single_user", create_at=0, update_at=0)
            users.append(user)
        else:
            # Fetch user from the database or service
            user = next((u for u in users_data if u.id == user_id), None)
            if user:
                users.append(user)

    # Sanitize user data based on permissions
    sanitized_users = []
    current_user_id = get_user_id()
    for user in users:
        if can_see_user(current_user_id, user.id):
            sanitized_users.append(user)

    return sanitized_users

@app.get("/users/me", response_model=User, responses={404: {"model": ErrorResponse}})
async def handle_get_me(team_id: Optional[str] = Query(None), channel_id: Optional[str] = Query(None)):
    """Returns the currently logged-in user"""
    user_id = get_user_id()
    
    user = next((u for u in users_data if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if team_id and has_permission_to(user_id, "manage_team"):
        user.permissions.append("manage_team")
    if has_permission_to(user_id, "manage_system"):
        user.permissions.append("manage_system")
    if channel_id and has_permission_to(user_id, "create_post"):
        user.permissions.append("create_post")

    return user

@app.get("/users/me/memberships", response_model=List[str])  # Replace str with actual Membership model
async def handle_get_my_memberships():
    """Returns the currently logged-in user's board memberships"""
    user_id = get_user_id()
    # Simulate fetching memberships
    memberships = ["membership_1", "membership_2"]  # Replace with actual fetching logic
    return memberships

@app.get("/users/{user_id}", response_model=User, responses={404: {"model": ErrorResponse}})
async def handle_get_user(user_id: str):
    """Returns a user"""
    user = next((u for u in users_data if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    current_user_id = get_user_id()
    if not can_see_user(current_user_id, user_id):
        raise HTTPException(status_code=404, detail="User ID not found")

    return user

@app.patch("/users/{user_id}/config", response_model=User, responses={404: {"model": ErrorResponse}})
async def handle_update_user_config(user_id: str, patch: UserPreferencesPatch):
    """Updates user config"""
    current_user_id = get_user_id()
    
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    user = next((u for u in users_data if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Apply patch logic (this is just a placeholder)
    # Update user preferences based on the patch
    return user

@app.get("/users/me/config", response_model=dict)  # Replace dict with actual Preferences model
async def handle_get_user_preferences():
    """Returns user preferences"""
    user_id = get_user_id()
    # Simulate fetching user preferences
    preferences = {"theme": "dark"}  # Replace with actual fetching logic
    return preferences
