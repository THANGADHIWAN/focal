from fastapi import FastAPI, Depends, HTTPException, Body, Path
from pydantic import BaseModel
from typing import List, Optional
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

# Models
class Subscription(BaseModel):
    subscriber_id: str
    block_id: str

class User(BaseModel):
    user_id: str

class ErrorResponse(BaseModel):
    error: str

# Dependency to get the current user ID
def get_user_id():
    # Implement logic to retrieve the current user ID
    return "current_user_id"

# Placeholder for the application logic
async def get_block_by_id(block_id: str) -> Optional[str]:
    # Replace with actual logic to check if the block ID is valid
    return block_id if block_id else None

async def create_subscription(subscription: Subscription) -> Subscription:
    # Replace with actual logic to create a subscription
    return subscription

async def delete_subscription(block_id: str, subscriber_id: str) -> None:
    # Replace with actual logic to delete a subscription
    pass

async def get_subscriptions(subscriber_id: str) -> List[Subscription]:
    # Replace with actual logic to retrieve subscriptions
    return [Subscription(subscriber_id=subscriber_id, block_id="block1")]

@app.post("/subscriptions", response_model=User, responses={400: {"model": ErrorResponse}})
async def handle_create_subscription(sub: Subscription, user_id: str = Depends(get_user_id)):
    if user_id != sub.subscriber_id:
        raise HTTPException(status_code=400, detail="UserID and SubscriberID mismatch")

    if not await get_block_by_id(sub.block_id):
        raise HTTPException(status_code=400, detail=f"Invalid blockID: {sub.block_id}")

    new_subscription = await create_subscription(sub)
    logger.debug(f"CREATE subscription: {new_subscription}")
    return User(user_id=new_subscription.subscriber_id)

@app.delete("/subscriptions/{block_id}/{subscriber_id}", responses={200: {}, 403: {"model": ErrorResponse}})
async def handle_delete_subscription(block_id: str, subscriber_id: str, user_id: str = Depends(get_user_id)):
    if user_id != subscriber_id:
        raise HTTPException(status_code=403, detail="Access denied")

    await delete_subscription(block_id, subscriber_id)
    logger.debug(f"DELETE subscription: blockID={block_id}, subscriberID={subscriber_id}")
    return {}

@app.get("/subscriptions/{subscriber_id}", response_model=List[Subscription], responses={403: {"model": ErrorResponse}})
async def handle_get_subscriptions(subscriber_id: str, user_id: str = Depends(get_user_id)):
    if user_id != subscriber_id:
        raise HTTPException(status_code=403, detail="Access denied")

    subs = await get_subscriptions(subscriber_id)
    logger.debug(f"GET subscriptions: subscriberID={subscriber_id}, count={len(subs)}")
    return subs

# To run the FastAPI app, use:
# `uvicorn filename:app --reload` (replace filename with your script name)
