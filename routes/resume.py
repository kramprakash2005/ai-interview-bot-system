from fastapi import APIRouter, UploadFile, File
from database.db import participants_collection, questions_collection, sessions_collection
from config import RESUME_STORAGE
import shutil

from services.resume_text_extractor import extract_resume_text
from services.resume_parser import parse_resume
from services.resume_question_generator import (
    generate_project_questions,
    generate_internship_questions
)
from services.project_selector import select_best_projects

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload/{participant_id}")
async def upload_resume(participant_id: str, file: UploadFile = File(...)):

    print("\n============================")
    print("Resume upload started")
    print("Participant:", participant_id)
    print("============================")

    # Validate file
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF resumes allowed"}

    file_path = f"{RESUME_STORAGE}/{participant_id}.pdf"

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("Resume saved at:", file_path)

    # Find participant
    participant = participants_collection.find_one({"_id": participant_id})

    if not participant:
        return {"error": "Participant not found"}

    session_id = participant["session_id"]

    session = sessions_collection.find_one({"_id": session_id})

    if not session:
        return {"error": "Session not found"}

    job_description = session.get("job_description", "")

    # Update resume path
    participants_collection.update_one(
        {"_id": participant_id},
        {"$set": {"resume_path": file_path}}
    )

    print("Resume path stored in DB")

    # Extract text
    resume_text = extract_resume_text(file_path)

    print("Resume text length:", len(resume_text))

    # Parse resume
    parsed_data = parse_resume(resume_text)

    projects = parsed_data.get("projects", [])
    internships = parsed_data.get("internships", [])

    print("Projects found:", len(projects))
    print("Internships found:", len(internships))

    # Select best projects
    selected_projects = select_best_projects(projects, job_description)

    print("Projects selected:", len(selected_projects))

    # Update participant record
    participants_collection.update_one(
        {"_id": participant_id},
        {"$set": {
            "projects": selected_projects,
            "internships": internships
        }}
    )

    print("Participant projects + internships updated")

    # Generate questions
    project_questions = generate_project_questions(selected_projects)
    internship_questions = generate_internship_questions(internships)

    print("\nGenerated Project Questions:")
    for q in project_questions:
        print(q)

    print("\nGenerated Internship Questions:")
    for q in internship_questions:
        print(q)

    # Insert project questions
    project_inserted = 0

    for q in project_questions:

        topic = q.get("topic")
        question = q.get("question")

        if not topic or not question:
            continue

        questions_collection.insert_one({
            "session_id": session_id,
            "participant_id": participant_id,
            "type": "PROJECT",
           "topic": topic,
           "text": question
        })

        project_inserted += 1

    # Insert internship questions
    internship_inserted = 0

    for q in internship_questions:

        topic = q.get("topic")
        question = q.get("question")

        if not topic or not question:
            continue

        questions_collection.insert_one({
            "session_id": session_id,
            "participant_id": participant_id,
            "type": "INTERNSHIP",
            "topic": topic,
            "text": question
        })

        internship_inserted += 1

    print("\nQuestions inserted into DB")
    print("Project questions stored:", project_inserted)
    print("Internship questions stored:", internship_inserted)

    print("============================\n")

    return {
        "message": "Resume processed successfully",
        "projects_selected": len(selected_projects),
        "project_questions": project_inserted,
        "internship_questions": internship_inserted
    }