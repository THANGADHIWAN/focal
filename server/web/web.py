from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

class WebServer:
    def __init__(self, app: FastAPI, static_dir: str, templates_dir: str):
        self.app = app
        self.static_dir = Path(static_dir)
        self.templates_dir = Path(templates_dir)
        self.templates = Jinja2Templates(directory=str(self.templates_dir))

        self.setup_routes()
        self.setup_static_files()

    def setup_routes(self):
        @self.app.get("/")
        async def index(request: Request):
            return self.templates.TemplateResponse("index.html", {"request": request})

        @self.app.get("/boards")
        async def boards(request: Request):
            return self.templates.TemplateResponse("boards.html", {"request": request})

        # Add more routes as needed

    def setup_static_files(self):
        self.app.mount("/static", StaticFiles(directory=str(self.static_dir)), name="static")

# Usage:
# app = FastAPI()
# web_server = WebServer(app, static_dir="path/to/static", templates_dir="path/to/templates")