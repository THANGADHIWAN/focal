from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import Optional, Union
import json

app = FastAPI()

# Define the SubscriberType as an Enum for validation
from enum import Enum

class SubscriberType(str, Enum):
    user = "user"
    channel = "channel"

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value in cls._value2member_map_

# Define BlockType (example implementation, you should adjust it)
class BlockType(str, Enum):
    board = "board"
    card = "card"

# Define the Subscription model using Pydantic
class Subscription(BaseModel):
    block_type: BlockType
    block_id: str
    subscriber_type: SubscriberType
    subscriber_id: str
    notified_at: Optional[int] = None
    create_at: int
    delete_at: int

    @validator('block_id', 'subscriber_id', 'block_type')
    def check_required_fields(cls, v, values, field):
        if not v:
            raise ValueError(f"Field '{field.name}' is required")
        return v

    def is_valid(self):
        if not self.block_id or not self.block_type or not self.subscriber_id:
            return False
        if not SubscriberType.is_valid(self.subscriber_type):
            return False
        return True

# Define the Subscriber model
class Subscriber(BaseModel):
    subscriber_type: SubscriberType
    subscriber_id: str
    notified_at: int

# Example route to create a Subscription
@app.post("/subscriptions/", response_model=Subscription)
async def create_subscription(subscription: Subscription):
    if not subscription.is_valid():
        raise HTTPException(status_code=400, detail="Invalid subscription")
    return subscription

# Example route to create a Subscriber
@app.post("/subscribers/", response_model=Subscriber)
async def create_subscriber(subscriber: Subscriber):
    return subscriber

# Example route to parse a JSON string into a Subscription
@app.post("/subscriptions/parse/")
async def parse_subscription(json_data: str):
    try:
        subscription = Subscription.parse_raw(json_data)
        return subscription
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")

# To run the FastAPI server, use:
# uvicorn filename:app --reload
