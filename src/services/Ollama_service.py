from ollama import chat
from typing import Dict
from services.user_memory import get_user_profile, update_user_profile, save_chat_message

class OllamaService:
    def __init__(self):
        pass  # We'll build prompt dynamically per request

    def build_system_message(self):
        user = get_user_profile()
        if not user or not user.get("name"):
            return """You are a helpful study assistant that provides advice on study techniques, time management, exam prep, and learning strategies. Keep responses concise, practical, and encouraging."""
        
        subjects = user.get("subjects") or "various subjects"
        return f"""You are a helpful study assistant.
The user's name is {user['name']}.
They are studying these subjects: {subjects}.
Their goals are: {user.get('goals', 'No specific goals provided')}.
Their preferred study style is: {user.get('study_style', 'Not specified')}.
Give advice tailored to their profile, encourage them, and keep responses concise."""

    def extract_profile_updates(self, user_input: str) -> Dict[str, str]:
        """
        Basic heuristic to detect new subjects or goals mentioned by user in their input.
        (In real app, use NLP or entity extraction)
        """
        lower = user_input.lower()
        updates = {}

        # Simple keywords that hint the user added a subject
        subject_keywords = ["chemistry", "arabic", "math", "physics", "biology", "history", "english"]

        # Append subject if mentioned and not already present
        current_subjects = get_user_profile().get("subjects", "").lower()
        for kw in subject_keywords:
            if kw in lower and kw not in current_subjects:
                if "subjects" in updates:
                    updates["subjects"] += f", {kw.capitalize()}"
                else:
                    updates["subjects"] = kw.capitalize()

        # You can add similar checks for goals or study style if needed

        return updates

    def generate_response(self, user_input: str) -> Dict[str, str]:
        try:
            # Try to detect if user input contains new profile info
            updates = self.extract_profile_updates(user_input)
            if updates:
                update_user_profile(**updates)

            system_message = self.build_system_message()

            # Retrieve some recent chat history to feed LLM context
            # (Optional: for demo keep empty or short)
            messages = [{"role": "system", "content": system_message},
                        {"role": "user", "content": user_input}]

            response = chat(model='llama3.2', messages=messages)

            # Save chat messages
            save_chat_message("user", user_input)
            save_chat_message("assistant", response['message']['content'])

            return {
                "status": "success",
                "message": response['message']['content']
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error generating response: {str(e)}"
            }

    def validate_credentials(self) -> bool:
        try:
            chat(model='llama3.2', messages=[{'role': 'user', 'content': 'test'}])
            return True
        except:
            return False
