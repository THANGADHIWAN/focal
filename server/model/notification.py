from datetime import datetime
from pydantic import BaseModel, ValidationError, validator
from typing import Optional


class BlockType(str):
    # Define the block types as needed (example types)
    BOARD = "board"
    CARD = "card"
    # Add other block types as necessary


class NotificationHint(BaseModel):
    block_type: BlockType
    block_id: str
    modified_by_id: str
    create_at: int  # Milliseconds since epoch
    notify_at: int  # Milliseconds since epoch

    @validator("block_id", "block_type", "modified_by_id")
    def check_not_empty(cls, v, field):
        if not v:
            raise ValueError(f"missing {field.name.replace('_', ' ')}")
        return v

    def is_valid(self):
        try:
            self.validate()
        except ValidationError as e:
            return False, e.errors()
        return True, None

    def copy(self):
        return NotificationHint(
            block_type=self.block_type,
            block_id=self.block_id,
            modified_by_id=self.modified_by_id,
            create_at=self.create_at,
            notify_at=self.notify_at,
        )

    def log_clone(self):
        return {
            "block_type": self.block_type,
            "block_id": self.block_id,
            "modified_by_id": self.modified_by_id,
            "create_at": datetime.fromtimestamp(self.create_at / 1000).strftime('%Y-%m-%d %H:%M:%S.%f'),
            "notify_at": datetime.fromtimestamp(self.notify_at / 1000).strftime('%Y-%m-%d %H:%M:%S.%f'),
        }


class ErrInvalidNotificationHint(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


# Example usage in a FastAPI app
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/notification_hint/")
async def create_notification_hint(notification_hint: NotificationHint):
    is_valid, errors = notification_hint.is_valid()
    if not is_valid:
        raise HTTPException(status_code=400, detail=errors)
    # Process the notification hint...
    return notification_hint
