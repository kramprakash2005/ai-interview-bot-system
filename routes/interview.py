from fastapi import APIRouter, HTTPException
from uuid import uuid4
from datetime import datetime

from database.db import (
    sessions_collection,
    questions_collection,
    participants_collection
)

from models.interview_models import AnswerRequest
from utils.stage_manager import get_next_stage
from services.evaluation_service import evaluate_interview

router = APIRouter(prefix="/interview", tags=["Interview"])


# -------------------------
# VALIDATE INVITE
# -------------------------
@router.post("/validate")
def validate_invite(invite_token: str, participant_id: str):

    p = participants_collection.find_one({
        "_id": participant_id,
        "invite_token": invite_token
    })

    if not p:
        raise HTTPException(400, "Invalid link")

    if p.get("invite_used"):
        raise HTTPException(400, "Link already used")

    participants_collection.update_one(
        {"_id": participant_id},
        {
            "$set": {
                "invite_used": True,
                "invite_used_at": datetime.utcnow()
            }
        }
    )

    return {"ok": True}


# -------------------------
# START INTERVIEW
# -------------------------
@router.post("/start/{participant_id}")
def start_interview(participant_id: str):

    participant = participants_collection.find_one({"_id": participant_id})

    if not participant:
        return {"error": "Participant not found"}

    if not participant.get("invite_used"):
        return {"error": "Invite not validated"}

    interview_id = str(uuid4())

    interview_session = {
        "session_id": interview_id,
        "participant_id": participant_id,
        "current_stage": "INTRO",
        "question_index": 0,
        "status": "active"
    }

    sessions_collection.insert_one(interview_session)

    intro_question = (
        "Please introduce yourself and briefly describe "
        "your background, skills, and key projects."
    )

    return {
        "session_id": interview_id,
        "stage": "INTRO",
        "question": intro_question
    }

@router.get("/{session_id}/next-question")
def get_next_question(session_id: str):

    interview_session = sessions_collection.find_one(
        {"session_id": session_id}
    )

    if not interview_session:
        return {"error": "Interview session not found"}

    stage = interview_session["current_stage"]
    index = interview_session["question_index"]
    participant_id = interview_session["participant_id"]

    participant = participants_collection.find_one(
        {"_id": participant_id}
    )

    if not participant:
        return {"error": "Participant not found"}

    job_session_id = participant["session_id"]

    # ---------------- INTRO -> move to first real stage ----------------

    if stage == "INTRO":

        next_stage = get_next_stage(stage)

        sessions_collection.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    "current_stage": next_stage,
                    "question_index": 0
                }
            }
        )

        stage = next_stage
        index = 0

    # ---------------- LOAD QUESTIONS ----------------

    if stage in ["PROJECT", "INTERNSHIP"]:

        questions = list(
            questions_collection.find({
                "session_id": job_session_id,
                "participant_id": participant_id,
                "type": stage
            })
        )

    else:

        questions = list(
            questions_collection.find({
                "session_id": job_session_id,
                "type": stage
            })
        )

    if not questions:
        return {"error": f"No questions found for stage {stage}"}

    # ---------------- STAGE FINISHED ----------------

    if index >= len(questions):

        next_stage = get_next_stage(stage)

        # interview finished
        if not next_stage:

            sessions_collection.update_one(
                {"session_id": session_id},
                {"$set": {"status": "completed"}}
            )

            return {
                "message": "Interview completed",
                "participant_id": participant_id
            }

        # move to next stage
        sessions_collection.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    "current_stage": next_stage,
                    "question_index": 0
                }
            }
        )

        stage = next_stage
        index = 0

        # reload questions for new stage
        if stage in ["PROJECT", "INTERNSHIP"]:

            questions = list(
                questions_collection.find({
                    "session_id": job_session_id,
                    "participant_id": participant_id,
                    "type": stage
                })
            )

        else:

            questions = list(
                questions_collection.find({
                    "session_id": job_session_id,
                    "type": stage
                })
            )

        if not questions:
            return {"error": f"No questions found for stage {stage}"}

    # ---------------- RETURN QUESTION ----------------

    question = questions[index]["text"]

    return {
        "stage": stage,
        "question": question
    }

# -------------------------
# SUBMIT ANSWER
# -------------------------
@router.post("/{session_id}/answer")
def submit_answer(session_id: str, body: AnswerRequest):

    interview_session = sessions_collection.find_one(
        {"session_id": session_id}
    )

    if not interview_session:
        return {"error": "Interview session not found"}

    participant_id = interview_session["participant_id"]

    answer_data = {
        "stage": interview_session["current_stage"],
        "question": body.question,
        "answer": body.answer
    }

    participants_collection.update_one(
        {"_id": participant_id},
        {"$push": {"answers": answer_data}}
    )

    sessions_collection.update_one(
        {"session_id": session_id},
        {"$inc": {"question_index": 1}}
    )

    return {"message": "Answer saved"}