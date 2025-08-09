"""
Utilities for handling file uploads and storage
"""
import os
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
from app.core.config import settings

async def save_upload_file(
    file: UploadFile,
    folder: str,
    max_size: Optional[int] = None
) -> str:
    """
    Save an uploaded file to the specified folder
    Returns the URL path to access the file
    """
    # Ensure upload directory exists
    upload_dir = Path(settings.UPLOAD_DIR) / folder
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Generate unique filename
    filename = file.filename
    file_path = upload_dir / filename
    counter = 1
    
    while file_path.exists():
        name, ext = os.path.splitext(filename)
        file_path = upload_dir / f"{name}_{counter}{ext}"
        counter += 1

    # Check file size if max_size provided
    if max_size:
        content = await file.read()
        if len(content) > max_size:
            raise ValueError(f"File size exceeds maximum allowed size of {max_size} bytes")
        file.file.seek(0)  # Reset file pointer

    # Save file
    async with file_path.open("wb") as f:
        while content := await file.read(8192):  # Read in 8KB chunks
            await f.write(content)

    # Return relative URL path
    return str(file_path.relative_to(settings.UPLOAD_DIR))
