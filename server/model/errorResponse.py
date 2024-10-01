from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware (optional, if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ErrorResponse Model
class ErrorResponse(BaseModel):
    error: str = None
    error_code: int = None

# Example endpoint that demonstrates error response
@app.get("/example/{item_id}")
async def example_endpoint(item_id: int):
    if item_id < 1:
        error_response = ErrorResponse(error="Invalid item ID", error_code=400)
        return JSONResponse(status_code=400, content=error_response.dict())
    return {"message": "Success"}

# Run the application
# Use 'uvicorn filename:app --reload' to run the app
