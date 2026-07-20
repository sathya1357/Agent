import streamlit as st
import ollama
import time
from PIL import Image
import pytesseract
from pathlib import Path
from db import init_db, save_message, load_messages, clear_messages

# Initialize DB
init_db()

# Configure pytesseract to use the user-local Tesseract installation if present
_tess_path = Path(r"C:\Users\sathy\AppData\Local\Programs\Tesseract-OCR\tesseract.exe")
if _tess_path.exists():
    pytesseract.pytesseract.tesseract_cmd = str(_tess_path)

st.set_page_config(page_title="Chatbot", layout="wide")
st.title("💬 My Personal Chatbot with OCR")

# Load messages
if "messages" not in st.session_state:
    st.session_state["messages"] = load_messages()

# --- Model selector dropdown ---
model_choice = st.selectbox(
    "Choose a model:",
    ["mistral", "llama2"],  # only include installed models
    index=0
)

# --- Helper function for streaming responses ---
def stream_response(messages, model):
    response_area = st.empty()
    agent_reply = ""
    buffer = ""

    for chunk in ollama.chat(model=model, messages=messages, stream=True):
        buffer += chunk["message"]["content"]

        # Flush when sentence boundary OR buffer too long
        if buffer.endswith((".", "?", "!", "\n")) or len(buffer) > 80:
            agent_reply += buffer
            response_area.markdown(agent_reply)
            buffer = ""
            time.sleep(0.3)

    # Add any leftover buffer
    agent_reply += buffer
    response_area.markdown(agent_reply)

    return agent_reply

# --- Input form (auto-clears after submit) ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_area("Type your message:", key="chat_input")
    submitted = st.form_submit_button("Send")

    if submitted and user_input.strip():
        # Save user message
        st.session_state["messages"].append({"role": "user", "content": user_input})
        save_message("user", user_input)

        # Get agent reply via helper function
        agent_reply = stream_response(st.session_state["messages"], model_choice)

        # Save agent reply
        st.session_state["messages"].append({"role": "assistant", "content": agent_reply})
        save_message("assistant", agent_reply)

# --- Image upload + OCR ---
uploaded_files = st.file_uploader("Upload images (PNG/JPG)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        text = pytesseract.image_to_string(image)

        st.markdown(f"**Extracted Text from {uploaded_file.name}:**")
        st.write(text)

        if text.strip():
            # Feed OCR text into chatbot
            st.session_state["messages"].append({"role": "user", "content": text})
            save_message("user", text)

            agent_reply = stream_response(st.session_state["messages"], model_choice)
            st.session_state["messages"].append({"role": "assistant", "content": agent_reply})
            save_message("assistant", agent_reply)

# --- Clear chat button ---
if st.button("🗑️ Clear Chat"):
    clear_messages()
    st.session_state["messages"] = []

# --- Display history with styled bubbles ---
st.markdown("### Chat History")

chat_container = st.container()
with chat_container:
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div style='text-align: right; background-color: #1E3A8A; color: white;
                padding: 12px; border-radius: 12px; margin: 6px; display: inline-block; max-width: 70%;'>
                {msg['content']}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style='text-align: left; background-color: #065F46; color: white;
                padding: 12px; border-radius: 12px; margin: 6px; display: inline-block; max-width: 70%;'>
                {msg['content']}
                </div>
                """,
                unsafe_allow_html=True,
            )
