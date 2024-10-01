from fastapi import FastAPI

app = FastAPI()

def make_card_link(server_root: str, team_id: str, board_id: str, card_id: str) -> str:
    """Creates fully qualified card links based on card ID and parents."""
    return f"{server_root}/team/{team_id}/{board_id}/0/{card_id}"

def make_board_link(server_root: str, team_id: str, board: str) -> str:
    """Creates a fully qualified board link based on team ID and board."""
    return f"{server_root}/team/{team_id}/{board}"

@app.get("/card_link")
def get_card_link(server_root: str, team_id: str, board_id: str, card_id: str):
    """API endpoint to get a card link."""
    link = make_card_link(server_root, team_id, board_id, card_id)
    return {"card_link": link}

@app.get("/board_link")
def get_board_link(server_root: str, team_id: str, board: str):
    """API endpoint to get a board link."""
    link = make_board_link(server_root, team_id, board)
    return {"board_link": link}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
