import json
import uuid
from fastapi import FastAPI
from datetime import datetime
from typing import List, Dict, Any, Optional

app = FastAPI()

class License:
    features: Optional[Dict[str, Any]] = None

class IDType:
    NONE = '7'
    TEAM = 't'
    BOARD = 'b'
    CARD = 'c'
    VIEW = 'v'
    SESSION = 's'
    USER = 'u'
    TOKEN = 'k'
    BLOCK = 'a'
    ATTACHMENT = 'i'

# Function to generate a new ID
def new_id(id_type: str) -> str:
    unique_id = str(uuid.uuid4()).replace('-', '')[:27]  # Simulating a 27-character ID
    return f"{id_type}{unique_id}"

# Convenience functions for time manipulation
def get_millis() -> int:
    return int(datetime.now().timestamp() * 1000)

def get_millis_for_time(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)

def get_time_for_millis(millis: int) -> datetime:
    return datetime.fromtimestamp(millis / 1000)

def seconds_to_millis(seconds: int) -> int:
    return seconds * 1000

def struct_to_map(obj: Any) -> Dict[str, Any]:
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))

def intersection(a: List[Any], b: List[Any]) -> List[Any]:
    return list(set(a) & set(b))

def get_intersection(*args: List[Any]) -> List[Any]:
    if not args:
        return []
    result = args[0]
    for lst in args[1:]:
        result = intersection(result, lst)
    return result

def is_cloud_license(license: License) -> bool:
    return license and license.features and license.features.get("cloud", False)

def dedupe_string_arr(arr: List[str]) -> List[str]:
    return list(set(arr))

def get_base_file_path() -> str:
    return f"boards/{datetime.now().strftime('%Y%m%d')}"

@app.get("/new_id/{id_type}")
def get_new_id(id_type: str):
    return {"new_id": new_id(id_type)}

@app.get("/current_millis")
def current_millis():
    return {"millis": get_millis()}

@app.get("/time_for_millis/{millis}")
def time_for_millis(millis: int):
    return {"datetime": get_time_for_millis(millis).isoformat()}

@app.post("/dedupe_strings")
def dedupe_strings(arr: List[str]):
    return {"deduped": dedupe_string_arr(arr)}

@app.get("/base_file_path")
def base_file_path():
    return {"base_file_path": get_base_file_path()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
