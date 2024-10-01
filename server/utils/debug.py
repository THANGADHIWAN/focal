import os
from fastapi import FastAPI

app = FastAPI()

def is_running_unit_tests() -> bool:
    testing = os.getenv("FOCALBOARD_UNIT_TESTING", "")
    return testing.lower() in ("1", "t", "y", "true", "yes")

@app.get("/is_running_unit_tests")
def check_unit_tests_status():
    return {"is_running_unit_tests": is_running_unit_tests()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
