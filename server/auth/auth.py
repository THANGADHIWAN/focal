from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Tuple
import time

# Assuming model.Session is a dataclass or similar structure
class Session(BaseModel):
    session_id: str
    user_id: str
    updated_at: int

# Configuration settings (you can customize this as needed)
class Configuration:
    def __init__(self, session_expire_time: int, session_refresh_time: int, enable_public_shared_boards: bool):
        self.session_expire_time = session_expire_time
        self.session_refresh_time = session_refresh_time
        self.enable_public_shared_boards = enable_public_shared_boards

# Mocking store and permissions services
class Store:
    def __init__(self):
        self.sessions = {}

    def get_session(self, token: str, expire_time: int) -> Optional[Session]:
        return self.sessions.get(token)

    def refresh_session(self, session: Session) -> None:
        session.updated_at = int(time.time())

    def get_sharing(self, board_id: str) -> Optional[dict]:
        # Mock sharing data for demonstration purposes
        return {"id": board_id, "enabled": True, "token": "valid_token"}

class PermissionsService:
    def has_permission_to_team(self, user_id: str, team_id: str, permission: str) -> bool:
        # Mock permission check for demonstration purposes
        return True

class Auth:
    def __init__(self, config: Configuration, store: Store, permissions: PermissionsService):
        self.config = config
        self.store = store
        self.permissions = permissions

    def get_session(self, token: str) -> Session:
        if len(token) < 1:
            raise HTTPException(status_code=400, detail="No session token provided")

        session = self.store.get_session(token, self.config.session_expire_time)
        if session is None:
            raise HTTPException(status_code=404, detail="Session not found")

        if session.updated_at < (time.time() * 1000 - self.config.session_refresh_time * 1000):
            self.store.refresh_session(session)

        return session

    def is_valid_read_token(self, board_id: str, read_token: str) -> Tuple[bool, Optional[Exception]]:
        sharing = self.store.get_sharing(board_id)
        if sharing is None:
            return False, None

        if not self.config.enable_public_shared_boards:
            return False, HTTPException(status_code=403, detail="Public shared boards disabled")

        if sharing["id"] == board_id and sharing["enabled"] and sharing["token"] == read_token:
            return True, None

        return False, None

    def does_user_have_team_access(self, user_id: str, team_id: str) -> bool:
        return self.permissions.has_permission_to_team(user_id, team_id, "view_team")

# Create FastAPI application
app = FastAPI()

# Configuration setup
config = Configuration(session_expire_time=3600, session_refresh_time=300, enable_public_shared_boards=True)
store = Store()
permissions_service = PermissionsService()
auth_service = Auth(config, store, permissions_service)

# Endpoints
@app.get("/session/{token}", response_model=Session)
async def get_session(token: str):
    return auth_service.get_session(token)

@app.get("/validate-token/{board_id}/{read_token}")
async def validate_token(board_id: str, read_token: str):
    is_valid, error = auth_service.is_valid_read_token(board_id, read_token)
    if error:
        raise error
    return {"valid": is_valid}

@app.get("/check-access/{user_id}/{team_id}")
async def check_user_access(user_id: str, team_id: str):
    has_access = auth_service.does_user_have_team_access(user_id, team_id)
    return {"access": has_access}
