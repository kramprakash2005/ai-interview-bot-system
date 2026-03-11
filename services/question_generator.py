import json
import re
from services.ollama_service import ask_ollama


def clean_llm_json(response: str):

    response = response.strip()

    response = re.sub(r"```json", "", response)
    response = re.sub(r"```", "", response)

    response = response.strip()

    if response.count("{") > response.count("}"):
        response += "}"

    return response


def generate_jd_questions(topics):

    topic_string = ", ".join(topics)

    prompt = f"""
You are a technical interviewer.

Generate short conceptual interview questions based on these topics.

Topics:
{topic_string}

Rules:
- Only ONE concept per question
- Do NOT include examples or coding tasks
- Do NOT combine multiple questions
- Maximum length: 15 words
- Focus on theory or understanding
- Only two questions per topic

Return JSON only.

Format:

{{
 "questions":[
  {{
   "topic":"",
   "question":""
  }}
 ]
}}
"""

    response = ask_ollama(prompt)

    print("\nRAW QUESTION RESPONSE:\n", response)

    try:

        response = clean_llm_json(response)

        data = json.loads(response)

        questions = data.get("questions", [])

        print("PARSED QUESTIONS:", len(questions))

        return questions

    except Exception as e:

        print("JSON parsing failed:", e)
        print("Cleaned response:", response)

        return []