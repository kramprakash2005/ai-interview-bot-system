from fastapi import APIRouter
from models.participant_model import ParticipantCreate
from database.db import participants_collection
import uuid

router = APIRouter(prefix="/participants", tags=["Participants"])

@router.post("/")
def create_participant(data: ParticipantCreate):

    participant_id = str(uuid.uuid4())

    participant = {
        "_id": participant_id,
        "session_id": data.session_id,
        "email": data.email,
        "name": data.name,
        "resume_path": None,
        "projects": [],
        "internships": [],
        "status": "invited"
    }

    participants_collection.insert_one(participant)

    return {"participant_id": participant_id}