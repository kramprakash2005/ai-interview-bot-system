from pydantic import BaseModel
from typing import List

class Answer(BaseModel):
    question: str
    answer: str
    stage: str


class InterviewSession(BaseModel):
    session_id: str
    participant_id: str
    current_stage: str
    question_index: int
    answers: List[Answer]
    status: str


class AnswerRequest(BaseModel):
    question: str
    answer: str