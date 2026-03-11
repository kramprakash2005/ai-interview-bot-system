from pydantic import BaseModel

class SessionCreate(BaseModel):
    title: str
    job_description: str