from fastapi import FastAPI, HTTPException, Request, Body
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import io

app = FastAPI()

# Mock models
class ChannelMember(BaseModel):
    channel_id: str
    user_id: str

class Reaction(BaseModel):
    user_id: str
    post_id: str
    emoji_name: str

class AppError(BaseModel):
    message: str
    detail_error: str
    status_code: int

class Channel(BaseModel):
    id: str
    name: str
    team_id: str

class Post(BaseModel):
    id: str
    channel_id: str
    message: str
    user_id: str

class User(BaseModel):
    id: str
    username: str
    email: str

class Team(BaseModel):
    id: str
    name: str
    display_name: str

# Mock API class
class MockAPI:
    @staticmethod
    async def add_channel_member(channel_id: str, user_id: str) -> Dict[str, Any]:
        return {"channel_id": channel_id, "user_id": user_id}

    @staticmethod
    async def add_reaction(reaction: Dict[str, Any]) -> Dict[str, Any]:
        return reaction

    @staticmethod
    async def add_user_to_channel(channel_id: str, user_id: str, post_root_id: str) -> Dict[str, Any]:
        return {"channel_id": channel_id, "user_id": user_id}

    @staticmethod
    async def create_channel(channel: Channel) -> Dict[str, Any]:
        return channel.dict()

    @staticmethod
    async def create_post(post: Post) -> Dict[str, Any]:
        return post.dict()

    @staticmethod
    async def get_channel(channel_id: str) -> Dict[str, Any]:
        return {"id": channel_id, "name": f"channel_{channel_id}", "team_id": f"team_{channel_id}"}

    @staticmethod
    async def get_post(post_id: str) -> Dict[str, Any]:
        return {"id": post_id, "channel_id": f"channel_{post_id}", "message": f"Message {post_id}", "user_id": f"user_{post_id}"}

    @staticmethod
    async def get_user(user_id: str) -> Dict[str, Any]:
        return {"id": user_id, "username": f"user_{user_id}", "email": f"user_{user_id}@example.com"}

    @staticmethod
    async def update_channel(channel: Channel) -> Dict[str, Any]:
        return channel.dict()

    @staticmethod
    async def update_post(post: Post) -> Dict[str, Any]:
        return post.dict()

    @staticmethod
    async def update_user(user: User) -> Dict[str, Any]:
        return user.dict()

    @staticmethod
    async def delete_channel(channel_id: str) -> Dict[str, Any]:
        return {"id": channel_id, "deleted": True}

    @staticmethod
    async def delete_post(post_id: str) -> Dict[str, Any]:
        return {"id": post_id, "deleted": True}

    @staticmethod
    async def delete_user(user_id: str) -> Dict[str, Any]:
        return {"id": user_id, "deleted": True}

    @staticmethod
    async def create_team(team: Team) -> Dict[str, Any]:
        return team.dict()

    @staticmethod
    async def get_team(team_id: str) -> Dict[str, Any]:
        return {"id": team_id, "name": f"team_{team_id}", "display_name": f"Team {team_id}"}

mock_api = MockAPI()

@app.post("/api/v4/channels/{channel_id}/members")
async def add_channel_member(channel_id: str, user_id: str):
    try:
        result = await mock_api.add_channel_member(channel_id, user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v4/reactions")
async def add_reaction(reaction: Reaction):
    try:
        result = await mock_api.add_reaction(reaction.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v4/channels/{channel_id}/members/user")
async def add_user_to_channel(channel_id: str, user_id: str, post_root_id: str = Body(...)):
    try:
        result = await mock_api.add_user_to_channel(channel_id, user_id, post_root_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v4/channels")
async def create_channel(channel: Channel):
    try:
        result = await mock_api.create_channel(channel)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v4/posts")
async def create_post(post: Post):
    try:
        result = await mock_api.create_post(post)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v4/channels/{channel_id}")
async def get_channel(channel_id: str):
    try:
        result = await mock_api.get_channel(channel_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v4/posts/{post_id}")
async def get_post(post_id: str):
    try:
        result = await mock_api.get_post(post_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v4/users/{user_id}")
async def get_user(user_id: str):
    try:
        result = await mock_api.get_user(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v4/channels/{channel_id}")
async def update_channel(channel_id: str, channel: Channel):
    try:
        channel.id = channel_id
        result = await mock_api.update_channel(channel)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v4/posts/{post_id}")
async def update_post(post_id: str, post: Post):
    try:
        post.id = post_id
        result = await mock_api.update_post(post)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v4/users/{user_id}")
async def update_user(user_id: str, user: User):
    try:
        user.id = user_id
        result = await mock_api.update_user(user)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v4/channels/{channel_id}")
async def delete_channel(channel_id: str):
    try:
        result = await mock_api.delete_channel(channel_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v4/posts/{post_id}")
async def delete_post(post_id: str):
    try:
        result = await mock_api.delete_post(post_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v4/users/{user_id}")
async def delete_user(user_id: str):
    try:
        result = await mock_api.delete_user(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v4/teams")
async def create_team(team: Team):
    try:
        result = await mock_api.create_team(team)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v4/teams/{team_id}")
async def get_team(team_id: str):
    try:
        result = await mock_api.get_team(team_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Helper function to convert Go-style errors to FastAPI exceptions
def handle_app_error(error: AppError):
    raise HTTPException(status_code=error.status_code, detail=error.message)
