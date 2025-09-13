# app.py
import streamlit as st
import google.generativeai as genai
from PIL import Image

# Corrected relative imports for files within the same 'src' package
from config import persona_instruction, faqs
from ui import load_css, render_sidebar

# --- Page & Theme Configuration ---
st.set_page_config(
    page_title="ScholarBot",
    page_icon="logo.png",
    layout="centered",
    initial_sidebar_state="auto",
)
load_css() # Load our custom CSS

# --- Asset & Secret Management ---
try:
    logo_image = Image.open("logo.png")
except FileNotFoundError:
    st.error("Logo image `logo.png` not found in the root directory.")
    logo_image = "✨"

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Error: Gemini API key is missing or invalid. Check your Streamlit secrets.", icon="🚨")
    st.stop()

# --- Model and Chat Initialization ---
model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=persona_instruction)

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am ScholarBot. Ask me about Master's scholarships abroad for Pakistani students."}]

# --- UI Rendering ---
st.title("ScholarBot")
status_placeholder = st.empty()
status_placeholder.text("Ready")

uploaded_file = render_sidebar()

# Display existing chat messages
for message in st.session_state.messages:
    avatar = logo_image if message["role"] == "assistant" else "👤"
    with st.chat_message(name=message["role"], avatar=avatar):
        st.markdown(message["content"])


# --- Core Logic: Handle New User Input ---
if prompt := st.chat_input("Ask about scholarships...") or st.session_state.pop("new_prompt", None):
    
    # 1. Append and display the user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 2. Generate and display the assistant's response in a new container
    with st.chat_message("assistant", avatar=logo_image):
        status_placeholder.text("Thinking...")
        assistant_response = None
        lower_case_prompt = prompt.lower()
        
        # A. Check for predefined, non-API responses
        if not uploaded_file and lower_case_prompt in faqs:
            assistant_response = faqs[lower_case_prompt]
        
        # B. If no predefined response, call the Generative AI
        if assistant_response:
            st.markdown(assistant_response)
        else:
            api_prompt_parts = [prompt]
            if uploaded_file:
                try:
                    image_to_send = Image.open(uploaded_file)
                    api_prompt_parts.append(image_to_send)
                except Exception as e:
                    st.error(f"Error processing image: {e}")
                    api_prompt_parts = [prompt] # Fallback to text-only

            # C. Call the API and handle the stream correctly
            try:
                response_placeholder = st.empty()
                response_stream = st.session_state.chat.send_message(api_prompt_parts, stream=True)
                
                full_response_parts = []
                for chunk in response_stream:
                    if chunk.text:
                        full_response_parts.append(chunk.text)
                        response_placeholder.markdown("".join(full_response_parts) + "▌") # Add a cursor effect
                
                # Final clean text without the cursor
                assistant_response = "".join(full_response_parts)
                response_placeholder.markdown(assistant_response)

            except Exception as e:
                print(f"AN ERROR OCCURRED: {e}")
                assistant_response = "Sorry, I've run into a technical issue. Please try your question again."
                st.error(assistant_response)

    # 3. Add the final assistant response to the chat history
    status_placeholder.text("Ready")
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    # 4. Rerun if an image was processed to reset the uploader state
    if uploaded_file:
        st.rerun()