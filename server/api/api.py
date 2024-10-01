from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import traceback

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Constants
HeaderRequestedWith = "X-Requested-With"
HeaderRequestedWithXML = "XMLHttpRequest"
ErrorNoTeamMessage = "No team"
ErrHandlerPanic = "HTTP handler panic"

# Dummy data and functions for demonstration
users = {}
single_user_token = ""

class ErrorResponse:
    def __init__(self, error: str, code: int):
        self.error = error
        self.error_code = code

# Dependency to get current user ID
def get_user_id(request: Request):
    session = request.state.session
    if session and "user_id" in session:
        return session["user_id"]
    return ""

@app.middleware("http")
async def add_session(request: Request, call_next):
    # Dummy session example
    request.state.session = {"user_id": "123"}  # Replace with actual session management
    response = await call_next(request)
    return response

@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception):
    logger.error(f"Exception occurred: {str(exc)}\n{traceback.format_exc()}")
    error_response = ErrorResponse("Internal server error", status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_response.__dict__)

@app.post("/api/v2/admin/users/{username}/password")
async def handle_admin_set_password(username: str, request_data: dict):
    try:
        password = request_data.get("password")
        if not password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is required")

        if username in users:
            users[username] = password  # Update password in dummy store
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        logger.debug(f"AdminSetPassword, username: {username}")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Password updated successfully"})

    except Exception as e:
        logger.error(f"Error in handle_admin_set_password: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@app.middleware("http")
async def panic_handler(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        logger.error("Http handler panic", exc_info=exc)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": ErrHandlerPanic})

@app.middleware("http")
async def require_csrf_token(request: Request, call_next):
    if request.headers.get(HeaderRequestedWith) != HeaderRequestedWithXML:
        logger.error("CSRF check failed")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "checkCSRFToken FAILED"})
    
    response = await call_next(request)
    return response

# Running the FastAPI server
# Use the command: uvicorn filename:app --reload
