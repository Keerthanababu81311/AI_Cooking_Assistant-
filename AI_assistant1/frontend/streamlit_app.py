import streamlit as st
from api import (
    clear_all_history,
    delete_history_item,
    ask_ai,
    ingredient_recipe,
    get_history,
    speech_to_text,
    text_to_speech
)
import base64
from streamlit_webrtc import webrtc_streamer

# --------------------------
# Page Config
# --------------------------

st.set_page_config(
    page_title="AI Cooking Assistant",
    page_icon="🍳",
    layout="wide"
)

st.markdown(
    """
    <div class="voice-container">
        <div class="voice-orb">
            🎤
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------
# Load CSS
# --------------------------

with open("styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# --------------------------
# Session State
# --------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "mic_active" not in st.session_state:
    st.session_state.mic_active = False

if "voice_mode" not in st.session_state:
    st.session_state.voice_mode = False

# --------------------------
# Sidebar
# --------------------------

with st.sidebar:

    st.title("🍳 AI Assistant")

    mode = st.radio(
        "Choose",
        [
            "AI Chat",
            "Ingredient Finder"
        ]
    )

    st.divider()

    st.subheader("📜 History")

    try:

        history = get_history()

        if history:

            for item in history[:10]:

                col1, col2 = st.columns([4, 1])

                with col1:
                    st.caption(
                        f"🍽 {item['recipe_name']}"
                    )

                with col2:
                    if st.button(
                        "❌",
                        key=f"delete_{item['id']}"
                    ):
                        delete_history_item(
                            item["id"]
                        )
                        st.rerun()

            st.divider()

            if st.button(
                "🗑️ Clear All History",
                use_container_width=True
            ):
                clear_all_history()
                st.rerun()

        else:
            st.caption("No history yet")

    except Exception as e:

        st.warning(
            f"Backend not running\n{e}"
        )

# --------------------------
# Header
# --------------------------

st.title("🍳 AI Cooking Assistant")

st.caption(
    "Ask cooking questions, get recipes, tips, and meal ideas"
)

col1, col2 = st.columns(2)

with col1:
    if st.button("🎤 Start Voice Mode"):
        st.session_state.voice_mode = True

with col2:
    if st.button("🛑 Stop Voice Mode"):
        st.session_state.voice_mode = False

if st.session_state.voice_mode:

    st.success("🎤 Voice Mode Active")

    webrtc_streamer(
        key="voice-chat",
        media_stream_constraints={
            "video": False,
            "audio": True
        }
    )

    try:

        voice_text = speech_to_text()

        if voice_text and voice_text.strip():

            prompt = voice_text

            with st.chat_message("user"):
                st.markdown(voice_text)

    except Exception:
        pass

# --------------------------
# Previous Messages
# --------------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------
# Chat Input
# --------------------------

prompt = st.chat_input(
    "Ask anything about cooking..."
)

# --------------------------
# Process Message
# --------------------------

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                if mode == "AI Chat":

                    result = ask_ai(
                        st.session_state.messages
                    )

                    response_data = result["response"]

                    reply = response_data.get(
                        "reply",
                        "Sorry, I could not generate a response."
                    )

                    timer_seconds = response_data.get(
                        "timer_seconds"
                    )

                    timer_message = response_data.get(
                        "timer_message"
                    )

                else:

                    result = ingredient_recipe(
                        prompt
                    )

                    reply = f"""
### 🥬 Detected Ingredients

{', '.join(result['ingredients'])}

### 🍽 Recommended Recipes

{result['recommendations']}
"""

                    timer_seconds = None
                    timer_message = None

                st.markdown(reply)

                if timer_seconds:

                    minutes = timer_seconds // 60

                    st.info(
                        f"⏱ Timer set for {minutes} minute(s)"
                    )

                    if timer_message:

                        st.caption(
                            f"🔔 Reminder: {timer_message}"
                        )

                try:

                    audio_response = text_to_speech(
                        str(reply)
                    )

                    if audio_response:

                        audio_base64 = base64.b64encode(
                            audio_response
                        ).decode()

                        st.markdown(
                            f"""
                            <audio autoplay>
                                <source
                                    src="data:audio/mp3;base64,{audio_base64}"
                                    type="audio/mp3">
                            </audio>
                            """,
                            unsafe_allow_html=True
                        )

                except Exception as voice_error:

                    st.warning(
                        f"Voice playback failed: {voice_error}"
                    )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": str(reply)
                    }
                )

            except Exception as e:

                st.error(
                    f"Backend connection failed\n\n{str(e)}"
                )