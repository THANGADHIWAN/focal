import os
import pathlib
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

# Setup logger
logger = logging.getLogger("uvicorn")

# Create FastAPI instance
app = FastAPI()

# Middleware for CORS (if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
base_prefix = os.getenv("FOCALBOARD_HTTP_SERVER_BASEPATH", "")
local_only = os.getenv("FOCALBOARD_LOCAL_ONLY", "false").lower() in ("true", "1")
port = int(os.getenv("FOCALBOARD_PORT", 8080))
ssl = os.getenv("FOCALBOARD_USE_SSL", "false").lower() in ("true", "1")

# Root path for static files
root_path = pathlib.Path(__file__).parent
base_url = os.getenv("FOCALBOARD_HTTP_SERVER_ROOT", "")

# Setup templates
templates = Jinja2Templates(directory=str(root_path))

# Serve static files
app.mount(f"{base_prefix}/static", StaticFiles(directory=str(root_path / "static")), name="static")

# Index route
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request, "BaseURL": base_url})
    except Exception as e:
        logger.error("Unable to serve the index.html file", exc_info=e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Start the application (optional; use uvicorn to run the server)
if __name__ == "__main__":
    import uvicorn

    addr = f"localhost:{port}" if local_only else f":{port}"
    logger.info(f"Starting server at http{'s' if ssl else ''}://{addr}")

    if ssl and os.path.exists("./cert/cert.pem") and os.path.exists("./cert/key.pem"):
        uvicorn.run(app, host="0.0.0.0", port=port, ssl_keyfile="./cert/key.pem", ssl_certfile="./cert/cert.pem")
    else:
        uvicorn.run(app, host="0.0.0.0", port=port)

