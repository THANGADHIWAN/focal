from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict
import logging

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Dummy user store for example purposes
users = {}

# Pydantic model for the password update request
class AdminSetPasswordData(BaseModel):
    password: str = Field(..., description="The new password for the user.")

# Dummy audit logging function
class AuditRecord:
    def __init__(self, action: str):
        self.action = action
        self.success = False
        self.metadata = {}

    def add_meta(self, key: str, value: str):
        self.metadata[key] = value

    def success_record(self):
        self.success = True
        logger.debug(f"Audit success for action: {self.action}, metadata: {self.metadata}")

    def fail_record(self):
        logger.warning(f"Audit fail for action: {self.action}, metadata: {self.metadata}")

# Endpoint to set user password
@app.put("/admin/set_password/{username}", response_model=Dict[str, str])
async def handle_admin_set_password(username: str, request_data: AdminSetPasswordData):
    audit_record = AuditRecord(action="adminSetPassword")
    audit_record.add_meta("username", username)

    # Validate password
    if not request_data.password:
        audit_record.fail_record()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is required")

    # Update the user password (dummy implementation)
    if username in users:
        users[username] = request_data.password
    else:
        audit_record.fail_record()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    logger.debug("AdminSetPassword, username: %s", username)

    # Log audit success
    audit_record.success_record()
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Password updated successfully"})

# To run the FastAPI server, use:
# uvicorn filename:app --reload
