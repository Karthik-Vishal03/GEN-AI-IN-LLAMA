import streamlit as st
from components.chat_interface import ChatInterface
from services.Ollama_service import OllamaService
from services.user_memory import init_db, get_user_profile, update_user_profile

# Initialize DB
init_db()

# Initialize services
chat_interface = ChatInterface()
ai_service = OllamaService()

# Page config
st.set_page_config(page_title="Study Assistant Bot", page_icon="📚", layout="wide")
st.title("🤖 Study Assistant Bot")
st.markdown("---")

# User profile management
user_profile = get_user_profile()

with st.sidebar:
    st.header("👤 Your Profile")
    if user_profile and user_profile.get("name"):
        st.write(f"**Name:** {user_profile.get('name')}")
        st.write(f"**Goals:** {user_profile.get('goals')}")
        st.write(f"**Subjects:** {user_profile.get('subjects')}")
        st.write(f"**Study Style:** {user_profile.get('study_style')}")
    else:
        st.info("No profile found. Please set up your profile below.")

    with st.form("profile_form", clear_on_submit=False):
        name = st.text_input("Your Name", value=user_profile.get("name", ""))
        goals = st.text_input("Study Goals", value=user_profile.get("goals", ""))
        subjects = st.text_input("Subjects (comma-separated)", value=user_profile.get("subjects", ""))
        study_style = st.selectbox("Study Style", ["Visual", "Auditory", "Kinesthetic", "Reading/Writing"], index=0)
        submit = st.form_submit_button("Save Profile")
        if submit and name and subjects:
            update_user_profile(name=name, goals=goals, subjects=subjects, study_style=study_style)
            st.success("Profile updated!")

    st.markdown("---")
    chat_interface.create_study_tips_sidebar()

# Display chat
chat_interface.display_messages()

# Handle user input
if user_input := chat_interface.get_user_input():
    chat_interface.add_message("user", user_input)
    st.chat_message("user").markdown(user_input)

    with st.spinner("Thinking..."):
        response = ai_service.generate_response(user_input)
        if response["status"] == "success":
            chat_interface.add_message("assistant", response["message"])
            st.chat_message("assistant").markdown(response["message"])
        else:
            st.error(response["message"])

st.markdown("---")
st.markdown("*Powered by LLaMA 3.2*")
