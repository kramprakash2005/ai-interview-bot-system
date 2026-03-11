import json
from services.ollama_service import ask_ollama


def select_best_projects(projects, job_description):

    if not projects:
        return []

    prompt = f"""
You are a technical recruiter.

From the following projects select the TWO most relevant ones for the job description.

Rules:
- Prefer projects matching the job description
- If none match, choose the most technically complex projects
- Return ONLY JSON

Format:

{{
 "selected_projects":[
  {{
   "name":"",
   "description":""
  }}
 ]
}}

Projects:
{projects}

Job Description:
{job_description}
"""

    response = ask_ollama(prompt)

    try:
        data = json.loads(response)
        return data["selected_projects"][:2]
    except:
        return projects[:2]