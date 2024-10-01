from fastapi import FastAPI, Depends
from pydantic import BaseModel

# Define your configuration model
class Config(BaseModel):
    auth_mode: str

class Server:
    def __init__(self, config: Config):
        self.config = config
        self.api = FastAPI()

        # Initialize the handlers
        self.init_handlers()

    def init_handlers(self):
        cfg = self.config
        self.api.mattermost_auth = cfg.auth_mode == "MattermostAuthMod"

    # You can define routes and handlers here
    @self.api.get("/auth-status")
    async def get_auth_status():
        return {"mattermost_auth": self.api.mattermost_auth}

# Example of initializing the server
if __name__ == "__main__":
    import uvicorn

    # Replace with actual configuration loading
    config = Config(auth_mode="MattermostAuthMod")
    server = Server(config=config)

    # Run the FastAPI app
    uvicorn.run(server.api, host="0.0.0.0", port=8000)
