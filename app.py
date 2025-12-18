import streamlit as st
from chatbot import get_bot_response
from PIL import Image
from predict_image import predict_image
import os

st.set_page_config(page_title="Local Chatbot", page_icon="")
st.title("Local Chatbot — Llama 3.2")

# Init session state keys
if "history" not in st.session_state:
    st.session_state.history = []

if "clear_text" not in st.session_state:
    st.session_state.clear_text = False

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "memory" not in st.session_state:
    st.session_state.memory = []

if st.session_state.clear_text:
    st.session_state.user_input = ""
    st.session_state.clear_text = False

chat_container = st.container()
thinking_container = st.container()


def build_memory_context():
    context = ""
    for turn in st.session_state.memory:
        context += f"User: {turn['user']}\n"
        context += f"Assistant: {turn['assistant']}\n"
    return context


def update_memory(user_text, bot_text, max_turns=5):
    st.session_state.memory.append({
        "user": user_text,
        "assistant": bot_text
    })
    if len(st.session_state.memory) > max_turns:
        st.session_state.memory = st.session_state.memory[-max_turns:]


with chat_container:
    for role, content in st.session_state.history:
        if role == "user_text":
            st.markdown(f"**You:** {content}")
        elif role == "user_image":
            col1, _ = st.columns([1,1])
            with col1:
                st.image(content, caption="You sent an image", use_container_width=True)
        elif role == "assistant_text":
            st.markdown(f"**Bot:** {content}")


with st.container():
    input_col, file_col, button_col = st.columns([6,1,1])

    with input_col:
        user_input = st.text_input(
            "",
            placeholder="Type a message...",
            key="user_input"
        )

    with file_col:
        uploaded_file = st.file_uploader(
            "",
            type=["png","jpg","jpeg"],
            key=f"upload_{st.session_state.uploader_key}",
            label_visibility="collapsed"
        )

    with button_col:
        send = st.button("Send")


if send and (user_input.strip() or uploaded_file):

    # handle text
    if user_input.strip():
        st.session_state.history.append(("user_text", user_input.strip()))

        with thinking_container:
            ph = st.markdown("**Bot:** thinking...")

        memory_context = build_memory_context()
        bot_reply = get_bot_response(
            memory_context + f"User: {user_input.strip()}\nAssistant:"
        )

        ph.empty()
        st.session_state.history.append(("assistant_text", bot_reply))
        update_memory(user_input.strip(), bot_reply)

    # handle image
    if uploaded_file:
        img = Image.open(uploaded_file)
        temp_path = "temp_user_image.jpg"
        img.save(temp_path)

        st.session_state.history.append(("user_image", img))

        with thinking_container:
            ph = st.markdown("**Bot:** analyzing image...")

        label = predict_image(temp_path)

        ph.empty()

        if label:
            with thinking_container:
                ph = st.markdown("**Bot:** thinking...")

            bot_reply = get_bot_response(
                f"Provide advice on how to handle this pest: {label}"
            )

            ph.empty()
            st.session_state.history.append(("assistant_text", bot_reply))
            update_memory(f"Pest detected: {label}", bot_reply)
        else:
            st.session_state.history.append(("assistant_text", "No pest detected."))

    st.session_state.clear_text = True

    st.session_state.uploader_key += 1

    st.rerun()