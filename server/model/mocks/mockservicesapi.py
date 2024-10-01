from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict

app = FastAPI()

# Define the models similar to the Go models
class TeamMember(BaseModel):
    id: str
    user_id: str
    team_id: str

class Post(BaseModel):
    id: str
    content: str

class Channel(BaseModel):
    id: str
    name: str

class User(BaseModel):
    id: str
    email: str
    username: str

class Preferences(BaseModel):
    theme: str
    notifications: bool

# Mock data storage
team_members: Dict[str, TeamMember] = {}
posts: Dict[str, Post] = {}
channels: Dict[str, Channel] = {}
users: Dict[str, User] = {}
preferences: Dict[str, Preferences] = {}

@app.post("/create_member", response_model=TeamMember)
async def create_member(user_id: str, team_id: str):
    member_id = f"member-{len(team_members) + 1}"
    new_member = TeamMember(id=member_id, user_id=user_id, team_id=team_id)
    team_members[member_id] = new_member
    return new_member

@app.post("/create_post", response_model=Post)
async def create_post(post: Post):
    posts[post.id] = post
    return post

@app.get("/get_channel/{channel_id}", response_model=Channel)
async def get_channel(channel_id: str):
    if channel_id in channels:
        return channels[channel_id]
    raise HTTPException(status_code=404, detail="Channel not found")

@app.post("/get_user_by_email", response_model=User)
async def get_user_by_email(email: str):
    for user in users.values():
        if user.email == email:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/get_preferences_for_user/{user_id}", response_model=Preferences)
async def get_preferences_for_user(user_id: str):
    if user_id in preferences:
        return preferences[user_id]
    raise HTTPException(status_code=404, detail="Preferences not found")

@app.put("/update_preferences_for_user/{user_id}", response_model=Preferences)
async def update_preferences_for_user(user_id: str, prefs: Preferences):
    preferences[user_id] = prefs
    return prefs

# Example of how to run the server
# Run this file with: uvicorn filename:app --reload
