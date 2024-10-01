from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI()

# Sample server metadata model
class ServerMetadata(BaseModel):
    version: str
    build_number: str
    build_date: str
    commit: str
    edition: str
    sku: str

# Dummy function to simulate getting server metadata
def get_server_metadata() -> ServerMetadata:
    return ServerMetadata(
        version="1.0.0",
        build_number="100",
        build_date="2023-01-01",
        commit="abc123",
        edition="community",
        sku="personal_server"
    )

@app.get("/hello", response_class=PlainTextResponse)
async def handle_hello():
    """Responds with `Hello` if the web service is running."""
    return "Hello"

@app.get("/ping", response_model=ServerMetadata)
async def handle_ping(single_user_token: str = None):
    """Responds with server metadata if the web service is running."""
    server_metadata = get_server_metadata()

    if single_user_token:
        server_metadata.sku = "personal_desktop"

    if server_metadata.edition == "plugin":
        server_metadata.sku = "suite"

    return server_metadata
