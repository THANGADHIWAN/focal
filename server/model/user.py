from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict, Optional
import json

app = FastAPI()

# Define the User model using Pydantic
class User(BaseModel):
    id: str
    username: str
    email: Optional[EmailStr] = Field(None, exclude=True)  # Excluded from serialization
    nickname: Optional[str] = None
    first_name: Optional[str] = Field(None, alias="firstname")
    last_name: Optional[str] = Field(None, alias="lastname")
    
    password: Optional[str] = Field(None, exclude=True)  # Excluded from serialization
    mfa_secret: Optional[str] = Field(None, exclude=True)  # Excluded from serialization
    auth_service: Optional[str] = Field(None, exclude=True)  # Excluded from serialization
    auth_data: Optional[str] = Field(None, exclude=True)  # Excluded from serialization
    
    create_at: Optional[int] = Field(None, alias="createAt")
    update_at: Optional[int] = Field(None, alias="updateAt")
    delete_at: int = Field(..., alias="deleteAt")
    is_bot: bool
    is_guest: bool
    permissions: Optional[List[str]] = None
    roles: str

    def sanitize(self, options: Dict[str, bool]):
        """Sanitize user data based on options."""
        self.password = None
        self.mfa_secret = None
        
        if options.get("email") is False:
            self.email = None
        if options.get("fullname") is False:
            self.first_name = None
            self.last_name = None

# Define the UserPreferencesPatch model
class UserPreferencesPatch(BaseModel):
    updated_fields: Optional[Dict[str, str]] = Field(None, alias="updatedFields")
    deleted_fields: Optional[List[str]] = Field(None, alias="deletedFields")

# Define the Session model
class Session(BaseModel):
    id: str
    token: str
    user_id: str = Field(..., alias="userID")
    auth_service: str = Field(..., alias="authService")
    props: Dict[str, any]
    create_at: Optional[int] = Field(None, alias="createAt")
    update_at: Optional[int] = Field(None, alias="updateAt")

# Example route to create a User
@app.post("/users/", response_model=User)
async def create_user(user: User):
    return user

# Example route to parse a User from JSON
@app.post("/users/parse/")
async def parse_user(json_data: str):
    try:
        user = User.parse_raw(json_data)
        return user
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")

# Example route to sanitize a User
@app.post("/users/sanitize/")
async def sanitize_user(user: User, options: Dict[str, bool]):
    user.sanitize(options)
    return user

# Example route to create a UserPreferencesPatch
@app.post("/user_preferences_patch/", response_model=UserPreferencesPatch)
async def create_user_preferences_patch(patch: UserPreferencesPatch):
    return patch

# Example route to create a Session
@app.post("/sessions/", response_model=Session)
async def create_session(session: Session):
    return session

# To run the FastAPI server, use:
# uvicorn filename:app --reload
