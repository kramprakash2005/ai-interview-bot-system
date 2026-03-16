from fastapi import APIRouter, HTTPException
from uuid import uuid4
from datetime import datetime

from database.db import (
    form_candidates_collection,
    participants_collection,
    sessions_collection
)

from services.email_service import send_invite_email


router = APIRouter(
    prefix="/form",
    tags=["Form Candidates"]
)


# =========================
# SUBMIT FORM (candidate)
# =========================

@router.post("/submit")
def submit_form(data: dict):

    required = ["session_id", "name", "email"]

    for r in required:
        if r not in data:
            raise HTTPException(400, f"Missing {r}")

    candidate = {
        "_id": str(uuid4()),
        "session_id": data["session_id"],
        "name": data["name"],
        "email": data["email"],
        "phone": data.get("phone"),
        "college": data.get("college"),
        "degree": data.get("degree"),
        "year": data.get("year"),
        "resume_path": None,
        "status": "pending",
        "approved": False,
        "created_at": datetime.utcnow()
    }

    form_candidates_collection.insert_one(candidate)

    return {"message": "Form submitted"}


# =========================
# GET BY SESSION
# =========================

@router.get("/by-session/{session_id}")
def get_by_session(session_id: str):

    data = list(
        form_candidates_collection.find(
            {"session_id": session_id},
            {"_id": 1, "name": 1, "email": 1, "status": 1}
        )
    )

    for d in data:
        d["_id"] = str(d["_id"])

    return data


# =========================
# APPROVE CANDIDATE
# =========================

@router.post("/approve/{candidate_id}")
def approve_candidate(candidate_id: str):

    candidate = form_candidates_collection.find_one(
        {"_id": candidate_id}
    )

    if not candidate:
        raise HTTPException(404, "Candidate not found")

    session_id = candidate["session_id"]

    session = sessions_collection.find_one(
        {"_id": session_id}
    )

    if not session:
        raise HTTPException(404, "Session not found")

    participant_id = str(uuid4())
    invite_token = str(uuid4())

    # move to participants collection

    participant = {

        "_id": participant_id,

        "session_id": session_id,

        "name": candidate["name"],

        "email": candidate["email"],

        "resume_path": None,

        "projects": [],

        "internships": [],

        "status": "invited",

        "invite_token": invite_token,

        "invite_used": False,

        "invite_used_at": None,
    }

    participants_collection.insert_one(participant)

    # send email

    link = (
        f"http://localhost:5500/welcome.html"
        f"?participant_id={participant_id}"
        f"&session_id={session_id}"
        f"&invite_token={invite_token}"
    )

    send_invite_email(
        candidate["email"],
        link,
        session["title"],
        ""
    )

    form_candidates_collection.update_one(
        {"_id": candidate_id},
        {
            "$set": {
                "status": "approved",
                "approved": True
            }
        }
    )

    return {"message": "Approved and invite sent"}


# =========================
# REJECT
# =========================

@router.post("/reject/{candidate_id}")
def reject_candidate(candidate_id: str):

    form_candidates_collection.update_one(
        {"_id": candidate_id},
        {
            "$set": {
                "status": "rejected",
                "approved": False
            }
        }
    )

    return {"message": "Rejected"}