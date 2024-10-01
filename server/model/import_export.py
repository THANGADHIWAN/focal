from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json

app = FastAPI()

class Block(BaseModel):
    # Define the structure of Block according to your requirements.
    pass

class Archive(BaseModel):
    version: int
    date: int
    blocks: List[Block]

class ArchiveHeader(BaseModel):
    version: int
    date: int

class ArchiveLine(BaseModel):
    type: str
    data: dict  # Use dict for raw JSON data

class ExportArchiveOptions(BaseModel):
    team_id: str
    board_ids: List[str] = []  # Empty list means export all boards

class ImportArchiveOptions(BaseModel):
    team_id: str
    modified_by: str
    board_modifier: str  # Replace with actual type
    block_modifier: str   # Replace with actual type

class ErrUnsupportedArchiveVersion(Exception):
    def __init__(self, got: int, want: int):
        self.got = got
        self.want = want

    def __str__(self):
        return f"unsupported archive version; got {self.got}, want {self.want}"

class ErrUnsupportedArchiveLineType(Exception):
    def __init__(self, line: int, got: str):
        self.line = line
        self.got = got

    def __str__(self):
        return f"unsupported archive line type; got {self.got}, line {self.line}"

@app.post("/export-archive/")
async def export_archive(options: ExportArchiveOptions):
    # Implementation for exporting an archive
    # For now, just return the options received
    return options

@app.post("/import-archive/")
async def import_archive(options: ImportArchiveOptions):
    # Example check for unsupported archive version
    if options.team_id == "unsupported":  # Example condition
        raise HTTPException(status_code=400, detail=str(ErrUnsupportedArchiveVersion(1, 2)))

    # Example check for unsupported archive line type
    # if some_condition:
    #     raise HTTPException(status_code=400, detail=str(ErrUnsupportedArchiveLineType(1, "invalid_type")))

    # Actual import logic here
    return options

# To run the app, use 'uvicorn filename:app --reload'
