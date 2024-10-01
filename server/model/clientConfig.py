from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Dict

app = FastAPI()

# Data model for ClientConfig
class ClientConfig(BaseModel):
    telemetry: bool = Field(..., title="Is telemetry enabled")
    telemetry_id: str = Field(..., alias="telemetryid", title="The telemetry ID")
    enable_public_shared_boards: bool = Field(..., title="Is public shared boards enabled")
    teammate_name_display: str = Field(..., title="Teammate name display")
    feature_flags: Dict[str, str] = Field(..., title="The server feature flags")
    max_file_size: int = Field(..., title="Required for file upload to check the size of the file")

# Example in-memory data storage
client_config_data = ClientConfig(
    telemetry=True,
    telemetry_id="your-telemetry-id",
    enable_public_shared_boards=True,
    teammate_name_display="full_name",
    feature_flags={"feature1": "enabled", "feature2": "disabled"},
    max_file_size=10485760  # 10 MB
)

# Endpoint to get the client configuration
@app.get("/client_config", response_model=ClientConfig)
async def get_client_config():
    return client_config_data

# Endpoint to update the client configuration
@app.post("/client_config", response_model=ClientConfig)
async def update_client_config(config: ClientConfig):
    global client_config_data
    client_config_data = config
    return client_config_data

# Run the application
# Use 'uvicorn filename:app --reload' to run the app
