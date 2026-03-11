from pydantic import BaseModel

class Evaluation(BaseModel):
    participant_id: str
    overall_score: int
    technical_depth: int
    communication: int
    summary: str