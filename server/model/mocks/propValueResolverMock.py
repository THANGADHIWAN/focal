from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

# Define a User model based on your application needs
class User(BaseModel):
    id: str
    username: str
    email: str

# Mock database for demonstration purposes
mock_db: Dict[str, User] = {
    "1": User(id="1", username="user1", email="user1@example.com"),
    "2": User(id="2", username="user2", email="user2@example.com"),
}

# Define the PropValueResolver interface equivalent
class PropValueResolver:
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Retrieve a user by their ID."""
        raise NotImplementedError

# Mock implementation of the PropValueResolver
class MockPropValueResolver(PropValueResolver):
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        user = mock_db.get(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

# FastAPI application
app = FastAPI()
resolver = MockPropValueResolver()

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: str):
    return resolver.get_user_by_id(user_id)

# Example of running the FastAPI app
# Use this command in terminal to run: uvicorn <your_script_name>:app --reload
