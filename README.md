# ScholarBot ✨ - A Conversational AI for Scholarship Guidance

https://scolarbotapp.streamlit.app/

ScholarBot is a state-of-the-art, multi-modal conversational AI architected to serve as a centralized, interactive, and user-friendly platform for Pakistani students seeking guidance on international Master's scholarships.

This project was developed for the Artificial Intelligence course at the University of the Punjab, Gujranwala Campus. It demonstrates a complete development lifecycle, from initial concept to a professionally structured, deployed, and robust final product. The core of the project is a powerful Large Language Model (Google Gemini-1.5-Flash) guided by a detailed persona and served through a polished, responsive user interface built with Streamlit.

---

## 🚀 Live Demo

Interact with the live, deployed version of ScholarBot here: **https://scolarbotapp.streamlit.app/**

---



## 🌟 Key Features 

ScholarBot has been engineered with a focus on reliability, user experience, and professional software design patterns.

🗣️ **Advanced Conversational AI:** The bot's intelligence is powered by the Google Gemini-1.5-Flash model. Instead of a brittle, keyword-based filter, the bot's behavior is governed by a **strict, detailed system persona**. This ensures it stays on topic, politely declines inappropriate requests, and maintains a professional, encouraging tone, allowing it to understand a wide range of user intents.

🧠 **Stateful Conversational Memory:** A robust state management system (`st.session_state`) provides a true multi-turn conversational memory, allowing for natural follow-up questions and context-aware dialogue.

🖼️ **Multi-modal Input:** Supports both text and image uploads, allowing users to ask for feedback on visual documents like CVs and resumes.

🎨 **Professional & Responsive UI:** A custom-themed, visually coherent dark mode interface built with custom CSS that works flawlessly on both desktop and mobile devices.

🔴 **Live Streaming Responses:** Assistant messages are streamed token-by-token with a typing indicator to create an engaging, real-time chat experience with robust error handling.

⚙️ **Intuitive User Controls:** Features a persistent sidebar with controls to start a "New Chat" and clickable "Example Prompts" to guide new users.

---

## 🛠️ Technology Stack

*   **Core Language:** Python 3
*   **Web Framework / UI:** Streamlit
*   **Generative AI:** Google Gemini-1.5-Flash API
*   **Image Processing:** Pillow
*   **Version Control:** Git & GitHub
*   **Deployment:** Streamlit Community Cloud & GitHub Codespaces

---

## 📂 Project Structure

The project follows a professional, modular structure to ensure maintainability and separation of concerns.
scolarbot_streamlit/
├── src/
│ ├── app.py # Main Streamlit application logic
│ ├── config.py # Stores system persona and static data
│ └── ui.py # Functions for rendering the UI
│
├── .gitignore # Specifies files for Git to ignore
├── README.md # You are here!
└── requirements.txt # Project dependencies
