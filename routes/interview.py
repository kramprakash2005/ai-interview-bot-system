from fastapi import APIRouter, HTTPException

from database.db import (
    interview_sessions_collection,
    questions_collection,
    participants_collection,
)

import uuid


router = APIRouter(
    prefix="/interview",
    tags=["Interview"]
)


# =============================
# START INTERVIEW
# =============================

@router.post("/start")
def start_interview(participant_id: str, session_id: str):

    state = interview_sessions_collection.find_one(
        {"participant_id": participant_id}
    )

    if state:
        return state

    new_state = {

        "_id": str(uuid.uuid4()),

        "participant_id": participant_id,

        "session_id": session_id,

        "current_stage": "JD",

        "question_index": 0,

        "status": "running",
    }

    interview_sessions_collection.insert_one(new_state)

    return new_state


# =============================
# GET NEXT QUESTION
# =============================

@router.get("/next/{participant_id}")
def get_next_question(participant_id: str):

    state = interview_sessions_collection.find_one(
        {"participant_id": participant_id}
    )

    if not state:
        raise HTTPException(404, "Interview not started")

    session_id = state["session_id"]
    stage = state["current_stage"]
    index = state["question_index"]

    questions = list(

        questions_collection.find(
            {
                "session_id": session_id,
                "type": stage
            }
        )

    )

    if index >= len(questions):

        # move to next stage

        if stage == "JD":
            stage = "PROJECT"
        elif stage == "PROJECT":
            stage = "INTERNSHIP"
        elif stage == "INTERNSHIP":
            stage = "BEHAVIORAL"
        else:

            interview_sessions_collection.update_one(
                {"participant_id": participant_id},
                {"$set": {"status": "completed"}}
            )

            return {"status": "completed"}

        interview_sessions_collection.update_one(
            {"participant_id": participant_id},
            {
                "$set": {
                    "current_stage": stage,
                    "question_index": 0,
                }
            }
        )

        return get_next_question(participant_id)

    q = questions[index]

    return {
        "question": q["text"],
        "stage": stage,
        "index": index,
    }


# =============================
# SAVE ANSWER
# =============================

@router.post("/answer")
def save_answer(
    participant_id: str,
    question: str,
    answer: str,
):

    participants_collection.update_one(
        {"_id": participant_id},
        {
            "$push": {
                "answers": {
                    "question": question,
                    "answer": answer,
                }
            }
        },
    )

    interview_sessions_collection.update_one(
        {"participant_id": participant_id},
        {
            "$inc": {
                "question_index": 1
            }
        },
    )

    return {"saved": True}