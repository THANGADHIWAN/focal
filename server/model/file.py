from fastapi import FastAPI
from pydantic import BaseModel
import mimetypes
import time

app = FastAPI()

# FileInfo Model
class FileInfo(BaseModel):
    creator_id: str
    create_at: int
    update_at: int
    name: str
    extension: str
    mime_type: str

# Utility function to get the current time in milliseconds
def get_current_millis():
    return int(time.time() * 1000)

# Function to create FileInfo
def new_file_info(name: str) -> FileInfo:
    extension = name.rsplit('.', 1)[-1].lower() if '.' in name else ''
    mime_type = mimetypes.guess_type(name)[0] or ''
    now = get_current_millis()
    return FileInfo(
        creator_id="boards",
        create_at=now,
        update_at=now,
        name=name,
        extension=extension,
        mime_type=mime_type,
    )

# Example endpoint to create file info
@app.post("/file-info/", response_model=FileInfo)
async def create_file_info(name: str):
    return new_file_info(name)

# Run the application
# Use 'uvicorn filename:app --reload' to run the app
