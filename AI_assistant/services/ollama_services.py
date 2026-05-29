import requests
import json

def generate_recipe(user_prompt):

    prompt = f"""
    Generate a cooking recipe in STRICT JSON format.

    Return ONLY valid JSON.

    Example format:
    {{
        "dish": "Chicken Curry",
        "ingredients": ["Chicken", "Salt", "Onion"],
        "steps": [
            "Cut vegetables",
            "Cook chicken",
            "Serve hot"
        ]
    }}

    User request: {user_prompt}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    print("OLLAMA RAW RESPONSE:")
    print(data["response"])

    recipe = json.loads(data["response"])

    return recipe