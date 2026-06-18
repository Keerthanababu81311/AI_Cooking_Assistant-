from faster_whisper import WhisperModel
from gtts import gTTS

import tempfile
import json
import os


model = WhisperModel(
    "base.en",
    compute_type="int8"
)

def speech_to_text(audio_file):

    temp_name = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as temp:

            temp.write(audio_file)
            temp_name = temp.name

        segments, info = model.transcribe(
            temp_name,
            language="en",
            beam_size=1
        )

        print(
            f"Detected language: {info.language}"
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        return text.strip()

    finally:

        if temp_name and os.path.exists(temp_name):
            try:
                os.remove(temp_name)
            except:
                pass


def text_to_speech(text, output_path):

    try:

        if text is None:
            text = ""

        if isinstance(text, dict):
            text = json.dumps(text)

        text = str(text)

        tts = gTTS(
            text=text,
            lang="en",
            slow=False
        )

        tts.save(output_path)

        return output_path

    except Exception as e:

        print(
            f"TTS Error: {e}"
        )

        raise