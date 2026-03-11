import json
import re

def parse_llm_json(response: str):

    response = response.strip()

    # remove markdown blocks
    response = re.sub(r"```json", "", response)
    response = re.sub(r"```", "", response)

    # attempt normal parsing
    try:
        return json.loads(response)
    except:
        pass

    # try extracting JSON block
    start = response.find("{")
    end = response.rfind("}") + 1

    if start != -1 and end != -1:
        try:
            return json.loads(response[start:end])
        except:
            pass

    return None