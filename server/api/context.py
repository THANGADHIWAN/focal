from fastapi import FastAPI, Depends, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import socket

app = FastAPI()

# Custom middleware to store the connection in the request state
class ConnectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Store the connection in the request state
        request.state.connection = request.scope.get('client')
        
        # Process the request
        response: Response = await call_next(request)
        return response

# Dependency to retrieve the connection
def get_connection(request: Request):
    connection = request.state.connection
    if connection is None:
        return None
    return socket.fromfd(connection[1], socket.AF_INET, socket.SOCK_STREAM)

# Add middleware to the application
app.add_middleware(ConnectionMiddleware)

@app.get("/")
async def read_root(connection=Depends(get_connection)):
    if connection:
        return {"message": "Connection exists", "connection_info": str(connection)}
    return {"message": "No connection available"}
