import json
import re
from services.ollama_service import ask_ollama


def clean_llm_json(response: str):
    """
    Cleans LLM responses to ensure valid JSON.
    """

    response = response.strip()

    # Remove markdown blocks
    response = re.sub(r"```json", "", response)
    response = re.sub(r"```", "", response)

    response = response.strip()

    # Fix missing closing brace
    if response.count("{") > response.count("}"):
        response += "}"

    return response


def extract_topics(job_description: str):

    prompt = f"""
You are an expert technical recruiter.

Extract the key technical topics from the following job description.

Extract maximum of 5 important topics only.

Return ONLY JSON.

Format:
{{
 "topics":[]
}}

Job Description:
{job_description}
"""

    response = ask_ollama(prompt)

    print("\nRAW LLM RESPONSE:\n", response)

    try:
        response = clean_llm_json(response)

        data = json.loads(response)

        topics = data.get("topics", [])

        print("EXTRACTED TOPICS:", topics)

        return topics

    except Exception as e:

        print("JSON parsing failed:", e)
        print("Cleaned response:", response)

        return []