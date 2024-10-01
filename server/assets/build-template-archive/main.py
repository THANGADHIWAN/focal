from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import zipfile
import json
from typing import Optional

app = FastAPI()

# Constants
DEF_ARCHIVE_FILENAME = "templates.boardarchive"
VERSION_FILENAME = "version.json"
BOARD_FILENAME = "board.jsonl"
MIN_ARCHIVE_VERSION = 2
MAX_ARCHIVE_VERSION = 2

class ArchiveVersion(BaseModel):
    version: int
    date: int

class AppConfig(BaseModel):
    dir: str
    out: Optional[str] = DEF_ARCHIVE_FILENAME
    verbose: bool = False

@app.post("/create_archive")
async def create_archive(config: AppConfig):
    if not config.dir:
        raise HTTPException(status_code=400, detail="Source directory is required")

    try:
        version_data = get_version_file(config)
        archive_path = build(config, version_data)
        return {"message": f"Archive created: {archive_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_version_file(config: AppConfig):
    path = os.path.join(config.dir, VERSION_FILENAME)
    with open(path, 'r') as file:
        buf = file.read()

    version = ArchiveVersion.parse_raw(buf)
    
    if version.version < MIN_ARCHIVE_VERSION or version.version > MAX_ARCHIVE_VERSION:
        raise HTTPException(status_code=400, detail=f"Unsupported archive version; require between {MIN_ARCHIVE_VERSION} and {MAX_ARCHIVE_VERSION} inclusive, got {version.version}")

    return version

def build(config: AppConfig, version_data: ArchiveVersion):
    archive_path = config.out
    with zipfile.ZipFile(archive_path, 'w') as archive_zip:
        # Write the version file
        archive_zip.writestr(VERSION_FILENAME, version_data.json())

        # Each board is a subdirectory; write each to the archive
        for board_id in os.listdir(config.dir):
            board_path = os.path.join(config.dir, board_id)
            if os.path.isdir(board_path):
                write_board(archive_zip, board_id, config)
    return archive_path

def write_board(archive_zip: zipfile.ZipFile, board_id: str, config: AppConfig):
    # Copy the board's jsonl file first. BoardID is also the directory name.
    src_path = os.path.join(config.dir, board_id, BOARD_FILENAME)
    dest_path = os.path.join(board_id, BOARD_FILENAME)
    write_file(archive_zip, src_path, dest_path, config)

    # Write other files in the board directory
    for file_name in os.listdir(os.path.join(config.dir, board_id)):
        if file_name == BOARD_FILENAME:
            continue

        src_path = os.path.join(config.dir, board_id, file_name)
        dest_path = os.path.join(board_id, file_name)
        if os.path.isfile(src_path):
            write_file(archive_zip, src_path, dest_path, config)

def write_file(archive_zip: zipfile.ZipFile, src_path: str, dest_path: str, config: AppConfig):
    archive_zip.write(src_path, dest_path)
    if config.verbose:
        print(f"{dest_path} written")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
