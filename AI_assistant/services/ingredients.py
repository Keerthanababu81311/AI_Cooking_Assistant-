import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def detect_ingredients(text):

    prompt = f"""
    Extract ingredients from this text.

    Return ONLY JSON array.

    Text:
    {text}
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return json.loads(data["response"])