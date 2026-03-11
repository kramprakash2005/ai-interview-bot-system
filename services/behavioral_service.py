from services.ollama_service import ask_ollama
import json
import re


def clean_llm_json(response: str):

    response = response.strip()
    response = re.sub(r"```json", "", response)
    response = re.sub(r"```", "", response)
    response = response.strip()

    if response.count("{") > response.count("}"):
        response += "}"

    return response


def generate_behavioral_questions(topics):

    topic_string = ", ".join(topics)

    prompt = f"""
You are a technical interviewer.

Generate behavioral interview questions for a candidate applying for a role
that requires the following skills:

{topic_string}

Rules:
- Focus on teamwork, ownership, debugging, and problem solving
- Questions should relate to software engineering work
- Maximum 15 words
- Generate exactly 3 questions

Return JSON only.

Format:

{{
 "questions":[
  {{
   "topic":"behavioral",
   "question":""
  }}
 ]
}}
"""

    response = ask_ollama(prompt)

    print("\nRAW BEHAVIORAL RESPONSE:\n", response)

    try:

        response = clean_llm_json(response)

        data = json.loads(response)

        questions = data.get("questions", [])

        print("PARSED BEHAVIORAL QUESTIONS:", len(questions))

        return questions

    except Exception as e:

        print("Behavioral JSON parsing failed:", e)

        return []