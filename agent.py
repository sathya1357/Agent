import streamlit as st
import ollama

st.title("My Local Agent")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("You:", "")

if st.button("Send") and user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    response = ollama.chat(model="mistral", messages=st.session_state["messages"])
    st.session_state["messages"].append({"role": "assistant", "content": response["message"]["content"]})

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.write(f"**You:** {msg['content']}")
    else:
        st.write(f"**Agent:** {msg['content']}")
