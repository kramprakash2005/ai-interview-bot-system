from services.ollama_service import ask_ollama
from services.json_utils import parse_llm_json


def parse_resume(resume_text: str):

    prompt = f"""
You are a resume extraction system.

Extract ALL software projects and ALL internships from the resume.

Important rules:
1. Identify the Projects section.
2. Extract EVERY project mentioned.
3. If the resume lists 3 projects, return 3 objects.
4. Never combine projects.
5. Do not omit any project.
6. The number of objects MUST equal the number of projects listed.

Return JSON ONLY.

Format:

{{
 "projects":[
  {{
   "name":"",
   "description":""
  }}
 ],
 "internships":[
  {{
   "company":"",
   "role":"",
   "description":""
  }}
 ]
}}

Resume:
{resume_text}
"""
    response = ask_ollama(prompt)

    if not response:
        print("LLM returned empty response")
        return {"projects": [], "internships": []}

    data = parse_llm_json(response)

    if not data:
        return {"projects": [], "internships": []}

    projects = data.get("projects", [])
    internships = data.get("internships", [])

    if not isinstance(projects, list):
        projects = []

    if not isinstance(internships, list):
        internships = []

    return {
        "projects": projects,
        "internships": internships
    }