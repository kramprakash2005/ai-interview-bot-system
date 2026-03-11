from fastapi import APIRouter
from database.db import participants_collection
from services.evaluation_service import evaluate_interview

router = APIRouter(prefix="/evaluation", tags=["Evaluation"])


@router.get("/{participant_id}")
def evaluate_candidate(participant_id: str):

    participant = participants_collection.find_one({"_id": participant_id})

    if not participant:
        return {"error": "Participant not found"}

    answers = participant.get("answers", [])

    if not answers:
        return {"error": "No answers found"}

    evaluation = evaluate_interview(answers)

    participants_collection.update_one(
        {"_id": participant_id},
        {"$set": {"evaluation": evaluation}}
    )

    return evaluation