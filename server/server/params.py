from pydantic import BaseModel, Field, root_validator, ValidationError
from typing import List, Optional
import logging

# Placeholder for Configuration class
class Configuration(BaseModel):
    # Define your configuration fields here (example)
    auth_mode: str = Field(..., alias="AuthMode")

# Placeholder for the Store class
class Store:
    # Placeholder for Store functionality
    pass

# Placeholder for the Logger class
class Logger:
    def __init__(self):
        self.logger = logging.getLogger("FocalBoardLogger")
        logging.basicConfig(level=logging.DEBUG)

    def debug(self, msg: str):
        self.logger.debug(msg)

    def error(self, msg: str):
        self.logger.error(msg)

# Placeholder for the WebSocket Adapter class
class WSAdapter:
    # Placeholder for WSAdapter functionality
    pass

# Placeholder for the Notify Backend class
class NotifyBackend:
    # Placeholder for NotifyBackend functionality
    pass

# Placeholder for the Permissions Service class
class PermissionsService:
    # Placeholder for PermissionsService functionality
    pass

# Placeholder for the Services API class
class ServicesAPI:
    # Placeholder for ServicesAPI functionality
    pass

class Params(BaseModel):
    cfg: Configuration
    single_user_token: str = Field(..., alias="SingleUserToken")
    db_store: Store = Field(..., alias="DBStore")
    logger: Logger
    server_id: str = Field(..., alias="ServerID")
    ws_adapter: WSAdapter = Field(..., alias="WSAdapter")
    notify_backends: List[NotifyBackend] = Field(..., alias="NotifyBackends")
    permissions_service: PermissionsService = Field(..., alias="PermissionsService")
    services_api: ServicesAPI = Field(..., alias="ServicesAPI")

    @root_validator
    def check_valid(cls, values):
        cfg, db_store, logger, permissions_service = (
            values.get("cfg"),
            values.get("db_store"),
            values.get("logger"),
            values.get("permissions_service"),
        )

        if cfg is None:
            raise ValueError("Cfg cannot be nil")
        if db_store is None:
            raise ValueError("DBStore cannot be nil")
        if logger is None:
            raise ValueError("Logger cannot be nil")
        if permissions_service is None:
            raise ValueError("PermissionsService cannot be nil")

        return values

class ErrServerParam(Exception):
    def __init__(self, name: str, issue: str):
        self.name = name
        self.issue = issue

    def __str__(self):
        return f"invalid server params: {self.name} {self.issue}"

# Function to simulate the server initialization with parameters
def init_server(params: Params):
    # Simulating server initialization logic
    if params.cfg.auth_mode == "MattermostAuthMod":
        params.logger.debug("Mattermost Authentication is enabled.")
    else:
        params.logger.debug("Using standard authentication.")

# Example of initializing Params
if __name__ == "__main__":
    # Replace with actual initialization of the configuration and services
    config = Configuration(auth_mode="MattermostAuthMod")  # Example initialization
    store = Store()  # Initialize your Store here
    logger = Logger()  # Initialize your Logger here
    ws_adapter = WSAdapter()  # Initialize your WSAdapter here
    notify_backends = [NotifyBackend()]  # Initialize your NotifyBackend(s) here
    permissions_service = PermissionsService()  # Initialize your PermissionsService here
    services_api = ServicesAPI()  # Initialize your ServicesAPI here

    try:
        params = Params(
            cfg=config,
            single_user_token="your_token_here",
            db_store=store,
            logger=logger,
            server_id="your_server_id",
            ws_adapter=ws_adapter,
            notify_backends=notify_backends,
            permissions_service=permissions_service,
            services_api=services_api,
        )
        init_server(params)
        print("Server initialized successfully.")
    except (ValueError, ValidationError) as e:
        logger.error(f"Error initializing parameters: {e}")
    except ErrServerParam as e:
        logger.error(f"Error: {e}")
