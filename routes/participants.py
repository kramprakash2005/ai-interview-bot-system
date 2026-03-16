from fastapi import APIRouter
from models.participant_model import ParticipantCreate
from database.db import participants_collection, sessions_collection

from services.email_service import send_invite_email

import uuid
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")

router = APIRouter(prefix="/participants", tags=["Participants"])


@router.post("/")
def create_participant(data: ParticipantCreate):

    participant_id = str(uuid.uuid4())
    invite_token = str(uuid.uuid4())

    session = sessions_collection.find_one(
        {"_id": data.session_id}
    )

    title = session["title"] if session else "Interview"
    desc = session.get("description", "") if session else ""

    # ✅ correct link
    link = (
        f"{FRONTEND_URL}/welcome.html"
        f"?participant_id={participant_id}"
        f"&session_id={data.session_id}"
        f"&invite_token={invite_token}"
    )

    participant = {

        "_id": participant_id,

        "session_id": data.session_id,

        "email": data.email,

        "name": data.name,

        "resume_path": None,

        "projects": [],

        "internships": [],

        "status": "invited",

        "invite_token": invite_token,

        "invite_used": False,

        "invite_used_at": None,
    }

    participants_collection.insert_one(participant)

    # send mail
    send_invite_email(
        data.email,
        link,
        title,
        desc,
    )

    return {
        "participant_id": participant_id
    }