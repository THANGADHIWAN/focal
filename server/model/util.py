from fastapi import FastAPI
from pydantic import BaseModel
import time
from datetime import datetime

app = FastAPI()

# Utility functions

def get_millis() -> int:
    """Get the current time in milliseconds since the epoch."""
    return int(time.time() * 1000)

def get_millis_for_time(this_time: datetime) -> int:
    """Get milliseconds since the epoch for the provided datetime."""
    return int(this_time.timestamp() * 1000)

def get_time_for_millis(millis: int) -> datetime:
    """Get a datetime object for milliseconds since the epoch."""
    return datetime.fromtimestamp(millis / 1000.0)

# Pydantic models for API responses
class MillisResponse(BaseModel):
    millis: int

class TimeResponse(BaseModel):
    time: datetime

@app.get("/current_millis/", response_model=MillisResponse)
async def current_millis():
    """Endpoint to get the current milliseconds since the epoch."""
    return MillisResponse(millis=get_millis())

@app.post("/millis_for_time/", response_model=MillisResponse)
async def millis_for_time(time: datetime):
    """Endpoint to get milliseconds since the epoch for a provided datetime."""
    return MillisResponse(millis=get_millis_for_time(time))

@app.post("/time_for_millis/", response_model=TimeResponse)
async def time_for_millis(millis: int):
    """Endpoint to get a datetime for milliseconds since the epoch."""
    return TimeResponse(time=get_time_for_millis(millis))

# To run the FastAPI server, use:
# uvicorn filename:app --reload
