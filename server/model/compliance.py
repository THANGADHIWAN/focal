from typing import List, Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

# Board model (simplified for demonstration)
class Board(BaseModel):
    id: str
    team_id: str
    # Add other fields as necessary

# BoardHistory model
class BoardHistory(BaseModel):
    id: str
    team_id: str
    is_deleted: bool
    descendant_last_update_at: int
    descendant_first_update_at: int
    created_by: str
    last_modified_by: str

# BlockHistory model
class BlockHistory(BaseModel):
    id: str
    team_id: str
    board_id: str
    type: str
    is_deleted: bool
    last_update_at: int
    first_update_at: int
    created_by: str
    last_modified_by: str

# BoardsComplianceResponse model
class BoardsComplianceResponse(BaseModel):
    has_next: bool
    results: List[Board]

# BoardsComplianceHistoryResponse model
class BoardsComplianceHistoryResponse(BaseModel):
    has_next: bool
    results: List[BoardHistory]

# BlocksComplianceHistoryResponse model
class BlocksComplianceHistoryResponse(BaseModel):
    has_next: bool
    results: List[BlockHistory]

# Query options for boards compliance
class QueryBoardsForComplianceOptions(BaseModel):
    team_id: Optional[str] = None
    page: int = Query(1, gt=0)  # Page number must be greater than 0
    per_page: int = Query(60, ge=1)  # Number of blocks per page must be at least 1

# Query options for boards compliance history
class QueryBoardsComplianceHistoryOptions(BaseModel):
    modified_since: int = 0
    include_deleted: bool = False
    team_id: Optional[str] = None
    page: int = Query(1, gt=0)
    per_page: int = Query(60, ge=1)

# Query options for blocks compliance history
class QueryBlocksComplianceHistoryOptions(BaseModel):
    modified_since: int = 0
    include_deleted: bool = False
    team_id: Optional[str] = None
    board_id: Optional[str] = None
    page: int = Query(1, gt=0)
    per_page: int = Query(60, ge=1)

# Sample endpoints (for demonstration)
@app.get("/boards/compliance", response_model=BoardsComplianceResponse)
async def get_boards_compliance(options: QueryBoardsForComplianceOptions):
    # Implement logic to retrieve boards compliance based on options
    return BoardsComplianceResponse(has_next=False, results=[])

@app.get("/boards/history/compliance", response_model=BoardsComplianceHistoryResponse)
async def get_boards_history_compliance(options: QueryBoardsComplianceHistoryOptions):
    # Implement logic to retrieve boards history compliance based on options
    return BoardsComplianceHistoryResponse(has_next=False, results=[])

@app.get("/blocks/history/compliance", response_model=BlocksComplianceHistoryResponse)
async def get_blocks_history_compliance(options: QueryBlocksComplianceHistoryOptions):
    # Implement logic to retrieve blocks history compliance based on options
    return BlocksComplianceHistoryResponse(has_next=False, results=[])

# Run the application
# Use 'uvicorn filename:app --reload' to run the app
