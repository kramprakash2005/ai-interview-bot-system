from fastapi import APIRouter
from uuid import uuid4

from database.db import (
    sessions_collection,
    questions_collection,
    participants_collection
)

from models.interview_models import AnswerRequest
from utils.stage_manager import get_next_stage

router = APIRouter(prefix="/interview", tags=["Interview"])


# -------------------------
# START INTERVIEW
# -------------------------
@router.post("/start/{participant_id}")
def start_interview(participant_id: str):

    interview_id = str(uuid4())

    interview_session = {
        "session_id": interview_id,
        "participant_id": participant_id,
        "current_stage": "JD",
        "question_index": 0,
        "status": "active"
    }

    sessions_collection.insert_one(interview_session)

    # find participant
    participant = participants_collection.find_one({"_id": participant_id})

    if not participant:
        return {"error": "Participant not found"}

    job_session_id = participant["session_id"]

    # first JD question
    first_question = questions_collection.find_one({
        "session_id": job_session_id,
        "type": "JD"
    })

    if not first_question:
        return {"error": "No JD questions found"}

    return {
        "session_id": interview_id,
        "stage": "JD",
        "question": first_question["text"]
    }


# -------------------------
# GET NEXT QUESTION
# -------------------------
@router.get("/{session_id}/next-question")
def get_next_question(session_id: str):

    interview_session = sessions_collection.find_one({"session_id": session_id})

    if not interview_session:
        return {"error": "Interview session not found"}

    stage = interview_session["current_stage"]
    index = interview_session["question_index"]
    participant_id = interview_session["participant_id"]

    # get participant
    participant = participants_collection.find_one({"_id": participant_id})

    if not participant:
        return {"error": "Participant not found"}

    job_session_id = participant["session_id"]

    # -------------------------
    # FETCH QUESTIONS
    # -------------------------
    if stage in ["PROJECT", "INTERNSHIP"]:

        questions = list(
            questions_collection.find({
                "session_id": job_session_id,
                "participant_id": participant_id,
                "type": stage
            })
        )

    else:  # JD + BEHAVIORAL

        questions = list(
            questions_collection.find({
                "session_id": job_session_id,
                "type": stage
            })
        )

    if not questions:
        return {"error": f"No questions found for stage {stage}"}

    # -------------------------
    # MOVE TO NEXT STAGE
    # -------------------------
    if index >= len(questions):

        next_stage = get_next_stage(stage)

        if not next_stage:

            sessions_collection.update_one(
                {"session_id": session_id},
                {"$set": {"status": "completed"}}
            )

            return {"message": "Interview completed"}

        sessions_collection.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    "current_stage": next_stage,
                    "question_index": 0
                }
            }
        )

        # fetch first question of next stage
        if next_stage in ["PROJECT", "INTERNSHIP"]:

            next_question = questions_collection.find_one({
                "session_id": job_session_id,
                "participant_id": participant_id,
                "type": next_stage
            })

        else:

            next_question = questions_collection.find_one({
                "session_id": job_session_id,
                "type": next_stage
            })

        return {
            "stage": next_stage,
            "question": next_question["text"] if next_question else None
        }

    # -------------------------
    # RETURN CURRENT QUESTION
    # -------------------------
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

    interview_session = sessions_collection.find_one({"session_id": session_id})

    if not interview_session:
        return {"error": "Interview session not found"}

    participant_id = interview_session["participant_id"]

    answer_data = {
        "stage": interview_session["current_stage"],
        "question": body.question,
        "answer": body.answer
    }

    # store answer in participant
    participants_collection.update_one(
        {"_id": participant_id},
        {"$push": {"answers": answer_data}}
    )

    # increment question index
    sessions_collection.update_one(
        {"session_id": session_id},
        {"$inc": {"question_index": 1}}
    )

    return {"message": "Answer saved"}