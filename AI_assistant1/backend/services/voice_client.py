import io
import wave
import time
import os
import threading
import tempfile

import requests
import numpy as np
import sounddevice as sd
import soundfile as sf
import webrtcvad

BASE_URL = "http://127.0.0.1:8000"

RATE = 16000
FRAME_MS = 30
FRAME_SIZE = int(RATE * FRAME_MS / 1000)

SILENCE_THRESHOLD = 500
MAX_SILENCE_FRAMES = 20

conversation = []
is_speaking = False


def play_voice(voice_bytes):

    global is_speaking

    is_speaking = True

    filename = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        ) as f:

            f.write(voice_bytes)
            filename = f.name

        print("\n🔊 Speaking...")

        data, samplerate = sf.read(
            filename,
            dtype="float32"
        )

        sd.play(
            data,
            samplerate
        )

        sd.wait()

    finally:

        is_speaking = False

        if filename and os.path.exists(filename):

            try:
                os.remove(filename)
            except:
                pass


def start_timer(seconds, message):

    def timer_worker():

        time.sleep(seconds)

        print(
            f"\n⏰ TIMER FINISHED: {message}"
        )

        try:

            voice = text_to_speech(
                message
            )

            play_voice(
                voice
            )

        except Exception as e:

            print(
                "Timer speech error:",
                e
            )

    threading.Thread(
        target=timer_worker,
        daemon=True
    ).start()


def pcm_to_wav_bytes(audio_pcm):

    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wf:

        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(audio_pcm)

    return buffer.getvalue()


def speech_to_text(wav_bytes):

    files = {
        "audio": (
            "voice.wav",
            wav_bytes,
            "audio/wav"
        )
    }

    response = requests.post(
        f"{BASE_URL}/speech-to-text",
        files=files,
        timeout=60
    )

    response.raise_for_status()

    return response.json()["text"]


def ask_ai(text):

    conversation.append(
        {
            "role": "user",
            "content": text
        }
    )

    response = requests.post(
        f"{BASE_URL}/ask",
        json={
            "messages": conversation
        },
        timeout=60
    )

    response.raise_for_status()

    data = response.json()["response"]

    conversation.append(
        {
            "role": "assistant",
            "content": data["reply"]
        }
    )

    return data


def text_to_speech(text):

    response = requests.post(
        f"{BASE_URL}/text-to-speech",
        json={
            "text": str(text)
        },
        timeout=60
    )

    response.raise_for_status()

    return response.content


def listen_until_silence():

    global is_speaking

    while is_speaking:
        time.sleep(0.1)

    print("\n🎤 Listening...")

    audio_chunks = []

    silence_frames = 0
    speech_started = False

    with sd.RawInputStream(
        samplerate=RATE,
        blocksize=FRAME_SIZE,
        dtype="int16",
        channels=1
    ) as stream:

        while True:

            data, _ = stream.read(
                FRAME_SIZE
            )

            frame = bytes(data)

            audio_np = np.frombuffer(
                frame,
                dtype=np.int16
            )

            volume = np.abs(
                audio_np
            ).mean()

            is_speech = (
                volume > SILENCE_THRESHOLD
            )

            if is_speech:

                speech_started = True
                silence_frames = 0

                audio_chunks.append(
                    frame
                )

            elif speech_started:

                silence_frames += 1

                audio_chunks.append(
                    frame
                )

                if silence_frames > MAX_SILENCE_FRAMES:
                    break

    return b"".join(audio_chunks)


print("=" * 50)
print("🤖 AI Voice Assistant Started")
print("🎤 Speak naturally")
print("Press CTRL+C to Exit")
print("=" * 50)

while True:

    try:

        pcm_audio = listen_until_silence()

        if len(pcm_audio) < 2000:
            continue

        wav_audio = pcm_to_wav_bytes(
            pcm_audio
        )

        text = speech_to_text(
            wav_audio
        )

        if not text.strip():
            continue

        print(
            f"\n🧑 You: {text}"
        )

        print(
            "\n🧠 Thinking..."
        )

        response = ask_ai(
            text
        )

        reply = response["reply"]

        print(
            f"\n🤖 AI: {reply}"
        )

        timer_seconds = response.get(
            "timer_seconds"
        )

        timer_message = response.get(
            "timer_message"
        )

        if timer_seconds:

            print(
                f"\n⏰ Timer Started: {timer_seconds} seconds"
            )

            start_timer(
                timer_seconds,
                timer_message
            )

        voice = text_to_speech(
            reply
        )

        play_voice(
            voice
        )

    except KeyboardInterrupt:

        print(
            "\n👋 Goodbye!"
        )

        break

    except Exception as e:

        print(
            "\n❌ Error:",
            e
        )

        time.sleep(2)