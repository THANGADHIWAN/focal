import logging
from fastapi import FastAPI

# Create a custom logging level
TELEMETRY_LOG_LEVEL = 9000
logging.addLevelName(TELEMETRY_LOG_LEVEL, "TELEMETRY")

def log_telemetry(self, message, *args, **kwargs):
    if self.isEnabledFor(TELEMETRY_LOG_LEVEL):
        self._log(TELEMETRY_LOG_LEVEL, message, args, **kwargs)

logging.Logger.telemetry = log_telemetry

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI()

@app.get("/")
async def read_root():
    logger.telemetry("Telemetry log message")
    return {"message": "Hello, World!"}

# To run the app, use 'uvicorn filename:app --reload'
