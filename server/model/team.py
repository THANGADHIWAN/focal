from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json

app = FastAPI()

# Define the Team model using Pydantic
class Team(BaseModel):
    id: str
    title: Optional[str] = None
    signup_token: str = Field(..., alias="signupToken")
    settings: Optional[Dict[str, Any]] = None
    modified_by: str = Field(..., alias="modifiedBy")
    update_at: int = Field(..., alias="updateAt")

# Function to parse JSON string into a Team object
def team_from_json(data: str) -> Team:
    return Team.parse_raw(data)

# Function to parse JSON string into a list of Team objects
def teams_from_json(data: str) -> List[Team]:
    return [Team.parse_obj(item) for item in json.loads(data)]

# Example route to create a Team
@app.post("/teams/", response_model=Team)
async def create_team(team: Team):
    return team

# Example route to parse a single Team from JSON
@app.post("/teams/parse/")
async def parse_team(json_data: str):
    try:
        team = team_from_json(json_data)
        return team
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")

# Example route to parse multiple Teams from JSON
@app.post("/teams/parse_multiple/")
async def parse_teams(json_data: str):
    try:
        teams = teams_from_json(json_data)
        return teams
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")

# To run the FastAPI server, use:
# uvicorn filename:app --reload
