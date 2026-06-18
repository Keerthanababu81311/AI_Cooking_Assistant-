import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:3b"

SYSTEM_PROMPT = """
You are a voice cooking assistant.

Always respond ONLY in valid JSON.

Example:

{
  "reply": "Fry the onions for 5 minutes.",
  "timer_seconds": 300,
  "timer_message": "The onions should be golden brown now. Stir them."
}

If no timer is needed:

{
  "reply": "Add salt and mix well.",
  "timer_seconds": null,
  "timer_message": null
}

Do not include markdown.
Do not include explanations outside JSON.
"""


def query_ollama(prompt):

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    return chat_with_ai(messages)


def chat_with_ai(messages):

    try:

        # Keep only recent conversation
        messages = messages[-10:]

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    }
                ] + messages,
                "stream": False,
                "options": {
                    "temperature": 0.5,
                    "num_predict": 300
                }
            },
            timeout=45
        )

        response.raise_for_status()

        data = response.json()

        content = (
            data["message"]["content"]
            .strip()
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:

            parsed = json.loads(content)

            return {
                "reply": str(
                    parsed.get(
                        "reply",
                        ""
                    )
                ),
                "timer_seconds": parsed.get(
                    "timer_seconds"
                ),
                "timer_message": parsed.get(
                    "timer_message"
                )
            }

        except Exception:

            return {
                "reply": content,
                "timer_seconds": None,
                "timer_message": None
            }

    except requests.exceptions.Timeout:

        return {
            "reply": "Sorry, I took too long to respond.",
            "timer_seconds": None,
            "timer_message": None
        }

    except Exception as e:

        return {
            "reply": f"AI Error: {str(e)}",
            "timer_seconds": None,
            "timer_message": None
        }