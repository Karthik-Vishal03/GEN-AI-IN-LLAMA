import streamlit as st
from typing import List, Dict

class ChatInterface:
    def __init__(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

    def display_messages(self):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def add_message(self, role: str, content: str):
        message = {"role": role, "content": content}
        st.session_state.messages.append(message)
        st.session_state.chat_history.append(message)

    def get_chat_history(self) -> List[Dict]:
        return st.session_state.chat_history

    def clear_chat(self):
        st.session_state.messages = []
        st.session_state.chat_history = []

    def create_study_tips_sidebar(self):
        with st.sidebar:
            st.header("Study Tips")
            st.info("""
            💡 Break tasks into smaller chunks  
            ⏰ Use the Pomodoro Technique  
            📝 Take active notes  
            🔄 Review regularly  
            """)
            if st.button("Clear Chat"):
                self.clear_chat()

    def get_user_input(self) -> str:
        return st.chat_input("Ask me anything about studying...")
