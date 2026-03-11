from services.ollama_service import ask_ollama
from services.json_utils import parse_llm_json


def extract_questions_from_text(text, topic):

    questions = []

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # remove numbering
        if line[0].isdigit():
            line = line.split(".", 1)[-1].strip()

        # skip JSON tokens
        if line in ["{", "}", "[", "]"]:
            continue

        if "questions" in line.lower():
            continue

        # remove quotes and commas
        line = line.strip('",')

        if len(line.split()) < 3:
            continue

        if len(line.split()) <= 20:

            questions.append({
                "topic": topic,
                "question": line
            })

    return questions


def generate_project_questions(projects):

    questions = []

    for project in projects:

        prompt = f"""
Generate two interview questions about this software project.

Project:
Name: {project.get("name","")}
Description: {project.get("description","")}

Rules:
- Focus on system design or architecture
- Maximum 15 words
- One question per line
- Do NOT explain anything

Return JSON only.

Format:
{{
 "questions": [
  "question1",
  "question2"
 ]
}}
"""

        response = ask_ollama(prompt)

        print("\nRAW PROJECT QUESTION RESPONSE:\n", response)

        data = parse_llm_json(response)

        if data and "questions" in data:

            for q in data["questions"]:

                if isinstance(q, str):

                    q_text = q.strip()

                    if q_text and len(q_text.split()) <= 20:

                        questions.append({
                            "topic": project.get("name", "Project"),
                            "question": q_text
                        })

        else:

            # fallback cleaner parser
            questions.extend(
                extract_questions_from_text(response, project.get("name", "Project"))
            )

    return questions


def generate_internship_questions(internships):

    if not internships:
        return []

    prompt = f"""
Generate two interview questions about this internship experience.

Internships:
{internships}

Rules:
- Ask about responsibilities
- Ask about challenges
- Maximum 15 words
- One question per line

Return JSON only.

Format:
{{
 "questions": [
  "question1",
  "question2"
 ]
}}
"""

    response = ask_ollama(prompt)

    print("\nRAW INTERNSHIP QUESTION RESPONSE:\n", response)

    data = parse_llm_json(response)

    questions = []

    if data and "questions" in data:

        for q in data["questions"]:

            if isinstance(q, str):

                q_text = q.strip()

                if q_text and len(q_text.split()) <= 20:

                    questions.append({
                        "topic": "Internship",
                        "question": q_text
                    })

    else:

        questions.extend(
            extract_questions_from_text(response, "Internship")
        )

    return questions