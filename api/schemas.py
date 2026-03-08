from pydantic import BaseModel


class DebugRequest(BaseModel):
    error: str


class DebugResponse(BaseModel):
    function: str | None = None
    file: str | None = None
    explanation: str
    suggested_fix: str