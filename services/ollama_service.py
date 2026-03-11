import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"   # change if needed


def ask_ollama(prompt: str):

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        if response.status_code != 200:
            print("Ollama HTTP error:", response.status_code)
            print(response.text)
            return ""

        data = response.json()

        return data.get("response", "")

    except Exception as e:

        print("Ollama request failed:", e)

        return ""