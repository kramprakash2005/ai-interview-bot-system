from pydantic import BaseModel

class AnswerCreate(BaseModel):
    participant_id: str
    question_id: str
    answer: str