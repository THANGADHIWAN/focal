from fastapi import FastAPI, Request, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional
import json
import logging

app = FastAPI()
logger = logging.getLogger("uvicorn")

# Define your data models
class LoginRequest(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    password: str
    mfa_token: Optional[str] = None
    type: str  # Can be "normal" or others

class LoginResponse(BaseModel):
    token: str

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    token: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

# Mock the app methods and auth services
class MockApp:
    async def login(self, username, email, password, mfa_token):
        # Mock login logic
        return "mock_token"

    async def logout(self, session_id):
        # Mock logout logic
        return True

    async def register_user(self, username, email, password):
        # Mock registration logic
        return True

    async def get_root_team(self):
        # Mock team retrieval
        return {"signup_token": "valid_token"}

    async def get_registered_user_count(self):
        # Mock user count retrieval
        return 0

app_service = MockApp()

# Middleware for attaching session (example implementation)
async def attach_session(request: Request):
    # Implement your session retrieval logic here
    return {"user_id": "mock_user", "session_id": "mock_session"}

@app.post("/login", response_model=LoginResponse)
async def handle_login(request: Request, login_data: LoginRequest):
    if login_data.type != "normal":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid login type")

    token = await app_service.login(login_data.username, login_data.email, login_data.password, login_data.mfa_token)
    return LoginResponse(token=token)

@app.post("/logout")
async def handle_logout(request: Request, session: dict = Depends(attach_session)):
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    await app_service.logout(session["session_id"])
    return {"message": "Logged out successfully"}

@app.post("/register")
async def handle_register(register_data: RegisterRequest):
    team = await app_service.get_root_team()

    if register_data.token and register_data.token != team["signup_token"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_count = await app_service.get_registered_user_count()
    if user_count > 0 and not register_data.token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No sign-up token and users already exist")

    await app_service.register_user(register_data.username, register_data.email, register_data.password)
    return {"message": "User registered successfully"}

@app.post("/users/{user_id}/changepassword")
async def handle_change_password(user_id: str, request_data: ChangePasswordRequest, session: dict = Depends(attach_session)):
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    # Implement password change logic
    return {"message": "Password changed successfully"}
