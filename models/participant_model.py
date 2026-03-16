from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ParticipantCreate(BaseModel):
    session_id: str
    name: Optional[str] = None
    email: str


class Participant(BaseModel):

    participant_id: str
    session_id: str
    email: str

    name: Optional[str] = None

    invite_token: Optional[str] = None
    invite_used: bool = False
    invite_used_at: Optional[datetime] = None