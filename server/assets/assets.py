from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Path to the embedded template archive
TEMPLATES_ARCHIVE_PATH = "templates.boardarchive"

@app.get("/default_templates")
async def get_default_templates():
    if not os.path.exists(TEMPLATES_ARCHIVE_PATH):
        raise HTTPException(status_code=404, detail="Templates archive not found")
    
    return FileResponse(TEMPLATES_ARCHIVE_PATH)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
