from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, EmailStr, validator
from typing import Optional

app = FastAPI()

MINIMUM_PASSWORD_LENGTH = 8

class ErrAuthParam(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg

class LoginRequest(BaseModel):
    type: str
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str
    mfa_token: Optional[str] = None

class LoginResponse(BaseModel):
    token: str

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    token: str

    @validator('username')
    def username_must_not_be_empty(cls, v):
        if not v.strip():
            raise ErrAuthParam("username is required")
        return v

    @validator('password')
    def password_must_meet_length(cls, v):
        if len(v) < MINIMUM_PASSWORD_LENGTH:
            raise ErrAuthParam(f"password must be at least {MINIMUM_PASSWORD_LENGTH} characters")
        return v

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

    @validator('old_password', 'new_password')
    def password_must_not_be_empty(cls, v):
        if not v:
            raise ErrAuthParam("password is required")
        return v

    @validator('new_password')
    def new_password_must_meet_length(cls, v):
        if len(v) < MINIMUM_PASSWORD_LENGTH:
            raise ErrAuthParam(f"password must be at least {MINIMUM_PASSWORD_LENGTH} characters")
        return v

@app.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    # Logic for handling login goes here
    return LoginResponse(token="example_token")

@app.post("/register")
async def register(request: RegisterRequest):
    # Logic for handling registration goes here
    return {"message": "User registered successfully"}

@app.post("/change-password")
async def change_password(request: ChangePasswordRequest):
    # Logic for handling password change goes here
    return {"message": "Password changed successfully"}

@app.exception_handler(ErrAuthParam)
async def auth_exception_handler(request, exc: ErrAuthParam):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
