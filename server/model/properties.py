# models.py
import json
from typing import Any, Dict, List, Optional, Union
from fastapi import HTTPException

class User:
    def __init__(self, user_id: str, username: str):
        self.id = user_id
        self.username = username

class BlockProp:
    def __init__(self, prop_id: str, name: str, value: str, index: int = 0):
        self.id = prop_id
        self.name = name
        self.value = value
        self.index = index

class PropDefOption:
    def __init__(self, prop_id: str, index: int, color: str, value: str):
        self.id = prop_id
        self.index = index
        self.color = color
        self.value = value

class PropDef:
    def __init__(self, prop_id: str, index: int, name: str, prop_type: str, options: Dict[str, PropDefOption]):
        self.id = prop_id
        self.index = index
        self.name = name
        self.type = prop_type
        self.options = options

    def get_value(self, v: Any, resolver: Optional['PropValueResolver']) -> str:
        if self.type == "select":
            if not isinstance(v, str):
                raise HTTPException(status_code=400, detail="Invalid property value type")
            opt = self.options.get(v)
            if not opt:
                raise HTTPException(status_code=400, detail="Invalid property value")
            return opt.value.upper()

        elif self.type == "date":
            if not isinstance(v, str):
                raise HTTPException(status_code=400, detail="Invalid property value type")
            return self.parse_date(v)

        elif self.type in ("person", "multiPerson"):
            user_ids = [v] if self.type == "person" else v
            usernames = []
            for user_id in user_ids:
                if resolver:
                    user = resolver.get_user_by_id(user_id)
                    usernames.append(user.username if user else user_id)
                else:
                    usernames.append(user_id)
            return ", ".join(usernames)

        raise HTTPException(status_code=400, detail="Unknown property type")

    def parse_date(self, s: str) -> str:
        # Assuming s is a JSON string with date details
        date_info = json.loads(s)
        date_str = f"{date_info['from']}"  # Replace with actual date formatting logic
        return date_str

class PropValueResolver:
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        pass  # This will be implemented in the resolver

class Board:
    def __init__(self, card_properties: List[Dict[str, Any]]):
        self.card_properties = card_properties

# Errors
class InvalidPropertyError(Exception):
    pass

class InvalidPropertyValueError(Exception):
    pass

class InvalidPropertyValueTypeError(Exception):
    pass


	# property_parsing.py
def parse_property_schema(board: Board) -> Dict[str, PropDef]:
    schema = {}
    for i, prop in enumerate(board.card_properties):
        prop_def = PropDef(
            prop_id=prop.get("id", ""),
            index=i,
            name=prop.get("name", ""),
            prop_type=prop.get("type", ""),
            options={opt["id"]: PropDefOption(opt["id"], j, opt["color"], opt["value"])
                     for j, opt in enumerate(prop.get("options", []))}
        )
        schema[prop_def.id] = prop_def
    return schema

def parse_properties(block: Dict[str, Any], schema: Dict[str, PropDef], resolver: PropValueResolver) -> Dict[str, BlockProp]:
    props = {}
    if not block:
        return props

    block_props = block.get("properties", {})
    if not isinstance(block_props, dict):
        raise InvalidPropertyError("Invalid properties")

    for k, v in block_props.items():
        prop = BlockProp(prop_id=k, name=k, value=str(v))
        if k in schema:
            try:
                prop.value = schema[k].get_value(v, resolver)
                prop.name = schema[k].name
                prop.index = schema[k].index
            except Exception as e:
                raise InvalidPropertyValueError(f"Could not parse property value: {e}")
        props[k] = prop
    return props

	# main.py
	from fastapi import FastAPI, HTTPException
	from models import Board, PropValueResolver
	from property_parsing import parse_property_schema, parse_properties
	
	app = FastAPI()
	
	@app.post("/boards/")
	async def create_board(card_properties: List[Dict[str, Any]]):
		board = Board(card_properties)
		schema = parse_property_schema(board)
		return {"schema": schema}
	
	@app.post("/blocks/")
	async def parse_block_properties(block: Dict[str, Any], schema: Dict[str, PropDef]):
		resolver = PropValueResolver()  # Implement this resolver with actual user fetching logic
		try:
			properties = parse_properties(block, schema, resolver)
			return {"properties": properties}
		except Exception as e:
			raise HTTPException(status_code=400, detail=str(e))
	
