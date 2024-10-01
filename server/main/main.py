import os
import signal
import time
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Replace with your actual logger configuration
import logging

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Global variables
p_server = None
time_between_pid_checks = 2

# Configuration model
class Config(BaseModel):
    port: int
    db_type: Optional[str] = None
    db_config_string: Optional[str] = None
    single_user_token: Optional[str] = None
    web_path: Optional[str] = None
    files_path: Optional[str] = None

# Load configuration from a JSON file
def read_config_file(file_path: str) -> Config:
    try:
        with open(file_path) as f:
            config_data = json.load(f)
        return Config(**config_data)
    except Exception as e:
        logger.error("Unable to read the config file: %s", e)
        raise

# Monitor PID function
def is_process_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True

def monitor_pid(pid: int):
    logger.info("Monitoring PID: %d", pid)
    
    while True:
        if not is_process_running(pid):
            logger.info("Monitored process not found, exiting.")
            os._exit(1)
        time.sleep(time_between_pid_checks)

# Start the server
@app.on_event("startup")
async def startup_event():
    # Read configuration
    config = read_config_file("config.json")  # Adjust the path as needed

    # Start monitoring process if required
    monitor_pid_pid = os.getenv("MONITOR_PID")
    if monitor_pid_pid and int(monitor_pid_pid) > 0:
        pid = int(monitor_pid_pid)
        monitor_pid(pid)

    # Set port and other configurations as needed
    if config.port:
        logger.info("Server starting on port: %d", config.port)
        # Initialize your database/store and other services here

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down server...")
    # Shutdown logic here

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Focalboard Server!"}

@app.post("/start")
async def start_server(config: Config):
    global p_server
    if p_server is not None:
        logger.info("Stopping existing server...")
        # Call stop_server() logic here

    # Configure the server
    logger.info("Starting server with config: %s", config.json())
    # Initialize your server here
    p_server = True  # Placeholder for server object

    return {"message": "Server started"}

@app.post("/stop")
async def stop_server():
    global p_server
    if p_server is None:
        raise HTTPException(status_code=400, detail="Server is not running")

    logger.info("Stopping server...")
    # Perform shutdown logic
    p_server = None
    return {"message": "Server stopped"}

# Signal handling for graceful shutdown
def signal_handler(sig, frame):
    logger.info("Signal received, shutting down...")
    os._exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)  # Adjust host and port as needed
