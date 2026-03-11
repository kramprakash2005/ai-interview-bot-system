from pydantic import BaseModel

class Question(BaseModel):
    session_id: str
    type: str
    topic: str
    text: str