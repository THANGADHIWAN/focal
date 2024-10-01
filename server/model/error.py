from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import List

app = FastAPI()

# Custom Error Classes
class NotFoundException(Exception):
    def __init__(self, entity: str):
        self.entity = entity

class NotAllFoundException(Exception):
    def __init__(self, entity: str, resources: List[str]):
        self.entity = entity
        self.resources = resources

class BadRequestException(Exception):
    def __init__(self, reason: str):
        self.reason = reason

class UnauthorizedException(Exception):
    def __init__(self, reason: str):
        self.reason = reason

class PermissionException(Exception):
    def __init__(self, reason: str):
        self.reason = reason

class ForbiddenException(Exception):
    def __init__(self, reason: str):
        self.reason = reason

class InvalidCategoryException(Exception):
    def __init__(self, msg: str):
        self.msg = msg

class NotImplementedException(Exception):
    def __init__(self, msg: str):
        self.msg = msg

# Exception Handlers
@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(status_code=404, content={"message": f"{exc.entity} not found"})

@app.exception_handler(NotAllFoundException)
async def not_all_found_exception_handler(request: Request, exc: NotAllFoundException):
    return JSONResponse(status_code=404, content={"message": f"Not all instances of {exc.entity} in {', '.join(exc.resources)} found"})

@app.exception_handler(BadRequestException)
async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(status_code=400, content={"message": exc.reason})

@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(status_code=401, content={"message": exc.reason})

@app.exception_handler(PermissionException)
async def permission_exception_handler(request: Request, exc: PermissionException):
    return JSONResponse(status_code=403, content={"message": exc.reason})

@app.exception_handler(ForbiddenException)
async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(status_code=403, content={"message": exc.reason})

@app.exception_handler(InvalidCategoryException)
async def invalid_category_exception_handler(request: Request, exc: InvalidCategoryException):
    return JSONResponse(status_code=400, content={"message": exc.msg})

@app.exception_handler(NotImplementedException)
async def not_implemented_exception_handler(request: Request, exc: NotImplementedException):
    return JSONResponse(status_code=501, content={"message": exc.msg})

# Example endpoint that raises exceptions
@app.get("/example/{entity}")
async def example_endpoint(entity: str):
    if entity == "not_found":
        raise NotFoundException(entity="Resource")
    elif entity == "bad_request":
        raise BadRequestException("Invalid request parameters.")
    elif entity == "unauthorized":
        raise UnauthorizedException("Access denied.")
    elif entity == "forbidden":
        raise ForbiddenException("You do not have permission.")
    return {"message": "Success"}

# Run the application
# Use 'uvicorn filename:app --reload' to run the app
