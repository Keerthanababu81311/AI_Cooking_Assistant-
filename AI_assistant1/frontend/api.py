import requests

BASE_URL = "http://127.0.0.1:8000"


def ask_ai(messages):

    try:

        response = requests.post(
            f"{BASE_URL}/ask",
            json={
                "messages": messages
            },
            timeout=45
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:

        raise Exception(
            f"AI request failed: {e}"
        )


def ingredient_recipe(prompt):

    try:

        response = requests.post(
            f"{BASE_URL}/ingredients",
            json={
                "prompt": prompt
            },
            timeout=45
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:

        raise Exception(
            f"Ingredient request failed: {e}"
        )


def get_history():

    try:

        response = requests.get(
            f"{BASE_URL}/history",
            timeout=15
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:

        raise Exception(
            f"History request failed: {e}"
        )


def delete_history_item(recipe_id):

    try:

        response = requests.delete(
            f"{BASE_URL}/history/{recipe_id}",
            timeout=15
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:

        raise Exception(
            f"Delete request failed: {e}"
        )


def clear_all_history():

    try:

        response = requests.delete(
            f"{BASE_URL}/history",
            timeout=15
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:

        raise Exception(
            f"Clear history failed: {e}"
        )


def speech_to_text(audio_file):

    try:

        files = {
            "audio": (
                "voice.wav",
                audio_file,
                "audio/wav"
            )
        }

        response = requests.post(
            f"{BASE_URL}/speech-to-text",
            files=files,
            timeout=120
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:

        raise Exception(
            f"Speech-to-text failed: {e}"
        )


def text_to_speech(text):

    try:

        response = requests.post(
            f"{BASE_URL}/text-to-speech",
            json={
                "text": str(text)
            },
            timeout=60
        )

        response.raise_for_status()

        return response.content

    except requests.exceptions.RequestException as e:

        raise Exception(
            f"Text-to-speech failed: {e}"
        )