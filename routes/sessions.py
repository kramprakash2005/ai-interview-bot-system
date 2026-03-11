from fastapi import APIRouter
from models.session_model import SessionCreate
from database.db import sessions_collection, questions_collection
from datetime import datetime
import uuid

from services.topic_extractor import extract_topics
from services.question_generator import generate_jd_questions

from services.behavioral_service import generate_behavioral_questions

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post("/")
def create_session(data: SessionCreate):

    session_id = str(uuid.uuid4())

    session = {
        "_id": session_id,
        "title": data.title,
        "job_description": data.job_description,
        "created_at": datetime.utcnow()
    }

    sessions_collection.insert_one(session)

    print("\n--- SESSION CREATED ---")
    print("Session ID:", session_id)

    # Extract topics
    topics = extract_topics(data.job_description)

    print("TOPICS:", topics)

    # Generate questions
    if not topics:
        print("No topics extracted. Skipping question generation.")
        questions = []
    else:
        jd_questions = generate_jd_questions(topics)

        behavioral_questions = generate_behavioral_questions(topics)

        questions = jd_questions + behavioral_questions

    print("QUESTIONS GENERATED:", len(questions))

    inserted_count = 0

    for q in questions:

        q_type = "BEHAVIORAL" if q.get("topic") == "behavioral" else "JD"

        questions_collection.insert_one({
            "session_id": session_id,
            "type": q_type,
            "topic": q.get("topic"),
            "text": q.get("question")
        })

        inserted_count += 1

    print("QUESTIONS STORED:", inserted_count)

    return {
        "session_id": session_id,
        "topics": topics,
        "questions_generated": inserted_count
    }