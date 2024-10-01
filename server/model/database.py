from enum import Enum
from fastapi import FastAPI

app = FastAPI()

class DatabaseType(str, Enum):
    sqlite = "sqlite3"
    postgres = "postgres"
    mysql = "mysql"

# Example endpoint using the DatabaseType enum
@app.get("/db-type/{db_type}", response_model=str)
async def get_db_type(db_type: DatabaseType):
    return f"Selected database type: {db_type.value}"

# Run the application
# Use 'uvicorn filename:app --reload' to run the app
