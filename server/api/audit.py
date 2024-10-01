from fastapi import Request, Depends
from typing import Optional, List, Dict

class AuditRecord:
    def __init__(self, api_path: str, event: str, status: str, user_id: str,
                 session_id: str, client: str, ip_address: str, meta: List[Dict[str, str]]):
        self.api_path = api_path
        self.event = event
        self.status = status
        self.user_id = user_id
        self.session_id = session_id
        self.client = client
        self.ip_address = ip_address
        self.meta = meta

class Session:
    def __init__(self, session_id: str, user_id: str):
        self.id = session_id
        self.user_id = user_id

async def get_current_session(request: Request) -> Optional[Session]:
    # Simulated session retrieval; replace with your actual implementation
    return request.state.session

def make_audit_record(request: Request, event: str, initial_status: str, team_id: str = "unknown") -> AuditRecord:
    session: Optional[Session] = request.state.session

    session_id = session.id if session else "unknown"
    user_id = session.user_id if session else "guest"

    record = AuditRecord(
        api_path=request.url.path,
        event=event,
        status=initial_status,
        user_id=user_id,
        session_id=session_id,
        client=request.headers.get("User-Agent", ""),
        ip_address=request.client.host,
        meta=[{"K": "team_id", "V": team_id}]
    )

    return record

# Example usage in an endpoint
@app.post("/some-endpoint")
async def some_endpoint(request: Request):
    audit_record = make_audit_record(request, "someEvent", "initialStatus")

    # Log or save the audit record as needed
    logger.debug(audit_record.__dict__)

    return {"message": "Success"}
