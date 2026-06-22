import json
import os
from datetime import datetime
from uuid import uuid4

from dotenv import load_dotenv
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv(".env")

MODEL_REPO_ID = "Qwen/Qwen2.5-7B-Instruct"
SYSTEM_PROMPT = "You are a helpful AI assistant."
CHAT_STORE_FILE = "chat_sessions.json"


def get_huggingface_token():
    return os.getenv("HUGGINGFACEHUB_API_TOKEN") or os.getenv(
        "HUGGINGFACEHUB_ACCESS_TOKEN"
    )


@st.cache_resource
def get_model(api_token):
    llm = HuggingFaceEndpoint(
        repo_id=MODEL_REPO_ID,
        task="text-generation",
        max_new_tokens=256,
        timeout=60,
        huggingfacehub_api_token=api_token,
    )
    return ChatHuggingFace(llm=llm)


def message_to_dict(message):
    if isinstance(message, HumanMessage):
        return {"role": "user", "content": message.content}
    if isinstance(message, AIMessage):
        return {"role": "assistant", "content": message.content}
    return {"role": "system", "content": message.content}


def dict_to_message(message):
    if message["role"] == "user":
        return HumanMessage(content=message["content"])
    if message["role"] == "assistant":
        return AIMessage(content=message["content"])
    return SystemMessage(content=message["content"])


def load_sessions():
    if not os.path.exists(CHAT_STORE_FILE):
        return []

    with open(CHAT_STORE_FILE, "r", encoding="utf-8") as file:
        sessions = json.load(file)

    saved_sessions = [
        session for session in sessions if session_has_user_message(session)
    ]
    if len(saved_sessions) != len(sessions):
        with open(CHAT_STORE_FILE, "w", encoding="utf-8") as file:
            json.dump(saved_sessions, file, indent=2)

    return saved_sessions


def save_sessions():
    sessions = [
        session
        for session in st.session_state.chat_sessions
        if session_has_user_message(session)
    ]
    with open(CHAT_STORE_FILE, "w", encoding="utf-8") as file:
        json.dump(sessions, file, indent=2)


def session_has_user_message(session):
    return any(message["role"] == "user" for message in session["messages"])


def create_new_session():
    session = {
        "id": str(uuid4()),
        "title": "New chat",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "messages": [message_to_dict(SystemMessage(content=SYSTEM_PROMPT))],
    }
    st.session_state.chat_sessions.insert(0, session)
    st.session_state.current_session_id = session["id"]
    st.session_state.chat_history = [SystemMessage(content=SYSTEM_PROMPT)]


def get_current_session():
    for session in st.session_state.chat_sessions:
        if session["id"] == st.session_state.current_session_id:
            return session
    return None


def load_session(session_id):
    st.session_state.current_session_id = session_id
    session = get_current_session()
    st.session_state.chat_history = [
        dict_to_message(message) for message in session["messages"]
    ]


def update_current_session():
    session = get_current_session()
    if not session:
        create_new_session()
        session = get_current_session()

    session["messages"] = [
        message_to_dict(message) for message in st.session_state.chat_history
    ]

    user_messages = [
        message.content
        for message in st.session_state.chat_history
        if isinstance(message, HumanMessage)
    ]
    if user_messages:
        session["title"] = user_messages[0][:40]

    save_sessions()


def init_chat_state():
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = load_sessions()

    if not st.session_state.chat_sessions:
        create_new_session()
        return

    if "current_session_id" not in st.session_state:
        st.session_state.current_session_id = st.session_state.chat_sessions[0]["id"]

    if "chat_history" not in st.session_state:
        load_session(st.session_state.current_session_id)


def render_chat_history():
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(message.content)


st.set_page_config(page_title="Personal Chatbot")
st.title("Personal Chatbot")

api_token = get_huggingface_token()
if not api_token:
    st.error("Set HUGGINGFACEHUB_ACCESS_TOKEN in .env before running this app.")
    st.stop()

init_chat_state()

with st.sidebar:
    st.subheader("Chat")

    if st.button("New chat", use_container_width=True):
        create_new_session()
        st.rerun()

    st.caption("Previous chats")
    for session in st.session_state.chat_sessions:
        if not session_has_user_message(session):
            continue

        is_current = session["id"] == st.session_state.current_session_id
        label = session["title"]
        if is_current:
            label = f"> {label}"

        if st.button(label, key=session["id"], use_container_width=True):
            if not is_current:
                load_session(session["id"])
                st.rerun()

render_chat_history()

user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    with st.chat_message("user"):
        st.write(user_input)

    model = get_model(api_token)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = model.invoke(st.session_state.chat_history)
                st.write(result.content)
                st.session_state.chat_history.append(AIMessage(content=result.content))
                update_current_session()
            except Exception as error:
                st.error(f"Unable to generate response: {error}")
