from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define version information
versions = [
    "8.0.0",
    "7.12.0",
    "7.11.1",
    "7.11.0",
    "7.10.0",
    "7.9.0",
    "7.8.0",
    "7.7.0",
    "7.6.0",
    "7.5.0",
    "7.4.0",
    "7.3.0",
    "7.2.0",
    "7.0.0",
    "0.16.0",
    "0.15.0",
    "0.14.0",
    "0.12.0",
    "0.11.0",
    "0.10.0",
    "0.9.4",
    "0.9.3",
    "0.9.2",
    "0.9.1",
    "0.9.0",
    "0.8.2",
    "0.8.1",
    "0.8.0",
    "0.7.3",
    "0.7.2",
    "0.7.1",
    "0.7.0",
    "0.6.7",
    "0.6.6",
    "0.6.5",
    "0.6.2",
    "0.6.1",
    "0.6.0",
    "0.5.0",
]

# Set current version and build information
CurrentVersion = versions[0]
BuildNumber = "1.0.0"  # Example value, replace as needed
BuildDate = "2024-10-01"  # Example value, replace as needed
BuildHash = "abc123"  # Example value, replace as needed
Edition = "Community"  # Example value, replace as needed

# Define a model to represent server information
class ServerInfo(BaseModel):
    version: str
    edition: str
    build_number: str
    build_date: str
    build_hash: str

# Endpoint to get server information
@app.get("/server_info/", response_model=ServerInfo)
async def get_server_info():
    server_info = ServerInfo(
        version=CurrentVersion,
        edition=Edition,
        build_number=BuildNumber,
        build_date=BuildDate,
        build_hash=BuildHash
    )
    logger.info("Focalboard server info retrieved: %s", server_info.json())
    return server_info

# Example logging call on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting Focalboard server")
    logger.info(
        "Focalboard server",
        extra={
            "version": CurrentVersion,
            "edition": Edition,
            "build_number": BuildNumber,
            "build_date": BuildDate,
            "build_hash": BuildHash
        }
    )

# To run the FastAPI server, use:
# uvicorn filename:app --reload
