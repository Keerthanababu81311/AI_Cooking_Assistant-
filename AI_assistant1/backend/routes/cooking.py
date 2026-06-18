from fastapi import APIRouter, HTTPException
from fastapi import UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel

from models.schema import CookingRequest

from services.ollama_services import chat_with_ai
from services.ingredients import detect_ingredients
from services.recoomendation_services import recommend_recipe

from services.memory_services import (
    save_recipe,
    get_history,
    delete_recipe,
    clear_history
)

from services.voice_service import (
    speech_to_text,
    text_to_speech
)

import tempfile

router = APIRouter()


# ----------------------------------
# TTS Request Model
# ----------------------------------

class TTSRequest(BaseModel):
    text: str


# ----------------------------------
# AI Chat
# ----------------------------------

@router.post("/ask")
def ask_ai(data: CookingRequest):

    try:

        messages = [
            msg.model_dump()
            for msg in data.messages
        ]

        response = chat_with_ai(
            messages
        )

        if not response:
            raise Exception(
                "Empty response from AI"
            )

        return {
            "response": response
        }

    except Exception as e:

        print("\n========== AI ERROR ==========")
        print(str(e))
        print("==============================\n")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ----------------------------------
# Speech To Text
# ----------------------------------

@router.post("/speech-to-text")
async def transcribe_audio(
    audio: UploadFile = File(...)
):

    try:

        audio_bytes = await audio.read()

        if not audio_bytes:
            raise HTTPException(
                status_code=400,
                detail="Audio file is empty"
            )

        text = speech_to_text(
            audio_bytes
        )

        return {
            "text": text
        }

    except Exception as e:

        print("\n========== STT ERROR ==========")
        print(str(e))
        print("===============================\n")

        raise HTTPException(
            status_code=500,
            detail=f"Speech recognition failed: {e}"
        )


# ----------------------------------
# Text To Speech
# ----------------------------------

@router.post("/text-to-speech")
def generate_audio(
    data: TTSRequest
):

    try:

        text = str(
            data.text
        ).strip()

        if not text:

            raise HTTPException(
                status_code=400,
                detail="Text cannot be empty"
            )

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        text_to_speech(
            text,
            temp_file.name
        )

        return FileResponse(
            path=temp_file.name,
            media_type="audio/mpeg",
            filename="response.mp3"
        )

    except Exception as e:

        print("\n========== TTS ERROR ==========")
        print(str(e))
        print("===============================\n")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ----------------------------------
# Ingredient Detection
# ----------------------------------

@router.post("/ingredients")
def ingredients(
    data: CookingRequest
):

    try:

        detected = [
            ingredient.lower()
            for ingredient in detect_ingredients(
                data.prompt
            )
        ]

        recommendations = recommend_recipe(
            detected
        )

        return {
            "ingredients": detected,
            "recommendations": recommendations
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ----------------------------------
# History
# ----------------------------------

@router.get("/history")
def history():

    try:

        return get_history()

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ----------------------------------
# Delete One History Item
# ----------------------------------

@router.delete("/history/{recipe_id}")
def delete_history(
    recipe_id: int
):

    try:

        delete_recipe(
            recipe_id
        )

        return {
            "message": "Deleted successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ----------------------------------
# Delete All History
# ----------------------------------

@router.delete("/history")
def delete_all_history():

    try:

        clear_history()

        return {
            "message": "All history deleted"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )