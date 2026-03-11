from pydantic import BaseModel
from typing import Optional

class ParticipantCreate(BaseModel):
    session_id: str
    name: Optional[str] = None
    email: str