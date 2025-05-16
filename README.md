# 🤖 Personalized Study Assistant Bot

A smart, AI-powered study assistant chatbot that evolves with you! This project uses [Streamlit](https://streamlit.io/) for the UI, [Ollama](https://ollama.com/) to run the LLaMA 3.2 model locally, and SQLite for storing a personalized user profile and chat history.

---

## ✨ Features

- **Personalized Assistance**  
  Learns about your goals, preferred subjects, and study style.

- **Single Profile Focus**  
  Designed for an individual user—no account management required.

- **Dynamic Profile Updates**  
  Automatically detects when you mention new subjects (like “I’m learning Chemistry”) and updates your profile.

- **Persistent Chat History**  
  All interactions are saved and can influence future responses.

- **Clean Streamlit UI**  
  Includes sidebar for setting and viewing your profile, and chat interface with study tips.

---

## 🧠 Tech Stack

| Component       | Tech Used            |
|----------------|----------------------|
| Frontend       | Streamlit            |
| Backend Model  | LLaMA 3.2 (via Ollama) |
| Database       | SQLite               |
| Language       | Python               |

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.8+
- Ollama installed locally with `llama3.2` model
- Install required Python packages:
            pip install streamlit ollama

2. Set up Ollama

Make sure Ollama is installed and running.
To install LLaMA 3.2: ollama pull llama3.2

Then start Ollama in the background: ollama serve

3. Run the App
streamlit run app.py

🗃️ Project Structure
.
├── main.py                 # Streamlit UI and app logic
├── components/
│   └── chat_interface.py   # Handles chat UI and message state
├── services/
│   ├── Ollama_service.py     # Chatbot logic and personalization prompt builder
│   └── user_memory.py      # SQLite DB logic for profile & chat history
├── study_bot.db            # SQLite database (auto-created)
└── README.md               # You're reading this!
