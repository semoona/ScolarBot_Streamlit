# app.py (Definitive Version: Image Uploader on Top)
import streamlit as st
import google.generativeai as genai
import re
from PIL import Image
import io

# --- Page & Theme Configuration ---
st.set_page_config(
    page_title="ScholarBot",
    page_icon="logo.png",
    layout="centered",
    initial_sidebar_state="auto",
)

# Load the logo image for use as the chat avatar.
try:
    logo_image = Image.open("logo.png")
except FileNotFoundError:
    st.error("Logo image `logo.png` not found. Please add it to the project folder.")
    logo_image = "✨"

# --- Final CSS Injection for Definitive Styling ---
st.markdown("""
<style>
    :root {
        --main-dark-bg: #0E1117;
        --functional-dark-bg: #262730;
        --text-color: #FAFAFA;
    }
    .stApp { background-color: var(--main-dark-bg); }
    [data-testid="stSidebar"] > div:first-child,
    [data-testid="chat-message-container"] { background-color: var(--functional-dark-bg); }
    [data-testid="chat-message-container"] { border: none; border-radius: 10px; }
    body, .stMarkdown, [data-testid="stMarkdownContainer"] p { color: var(--text-color); }
    .st-emotion-cache-1y4p8pa { align-items: center; }
    [data-testid="stStatusWidget"] > div { border: none; background: transparent; }
    .st-emotion-cache-10539ik { padding-left: 0px; color: #8A8D93; }
    .st-emotion-cache-1avcm0n h1 { color: var(--text-color); }
    @media (max-width: 640px) {
        .st-emotion-cache-1avcm0n h1 { display: none; }
        .st-emotion-cache-1y4p8pa { justify-content: center; }
    }
</style>
""", unsafe_allow_html=True)


# --- Secret Management ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Error configuring Gemini API: Key missing or invalid. Check Streamlit secrets.", icon="🚨")
    st.stop()

# --- FAQ & Keyword Filtering (No changes) ---
faqs = {
    "what scholarships are available?": "I can help with scholarships for Pakistani students! Some options include Chevening (UK), DAAD (Germany), Fulbright (USA), Erasmus Mundus (Europe), and Australia Awards (Australia). Ask about a specific scholarship or country!",
    "hello": "Hello! I’m ScholarBot, here to help Pakistani students find Master’s scholarships abroad. Ask me about scholarships like Chevening or DAAD!",
    "hi": "Hi there! I can help with Master’s scholarships for Pakistani students studying abroad. What would you like to know?",
    "thanks": "You’re welcome! Let me know if you have more questions about scholarships.",
    "thank you": "You’re welcome! Feel free to ask more about scholarships for studying abroad.",
    "help": "I can provide information about Master’s scholarships abroad for Pakistani students. Ask me about eligibility, application processes, deadlines, or specific countries like the UK, USA, Germany, etc.",
    "what can you do?": "I’m ScholarBot, specializing in Master’s scholarships for Pakistani students aiming to study overseas. I can help with eligibility, funding, deadlines, and more. Ask about scholarships like Chevening, DAAD, or Fulbright!",
    "how to apply for a scholarship?": "The application process depends on the scholarship. For example, Chevening requires an online application, essays, and references, while DAAD often needs a research proposal. Which scholarship are you interested in?",
    "what is the deadline for chevening?": "The deadline for the Chevening Scholarship is usually in November each year, likely November 2025 for the next cycle. Check their official website for exact dates: https://www.chevening.org.",
    "what scholarships are available in germany?": "For Pakistani students, the DAAD Scholarship is a great option in Germany. It offers a monthly stipend, travel allowance, and insurance. Deadlines vary by program, so check https://www.daad.de for details."
}
scholarship_keywords = [
    "scholarship", "scholar", "funding", "grant", "bursary", "fellowship",
    "master", "masters", "graduate", "postgraduate", "degree", "program",
    "abroad", "overseas", "international", "study", "education", "university",
    "pakistani", "pakistan", "student",
    "chevening", "daad", "fulbright", "erasmus", "australia awards",
    "uk", "usa", "germany", "europe", "australia", "japan", "korea", "malaysia",
    "canada", "france", "italy", "finland", "china", "thailand", "indonesia",
    "stipend", "tuition", "application", "deadline", "eligibility"
]
def is_scholarship_query(user_input):
    lower_case_input = user_input.lower()
    if any(keyword in lower_case_input for keyword in scholarship_keywords): return True
    if any(re.search(rf'\b{re.escape(keyword[:3])}\w*\b', lower_case_input) for keyword in scholarship_keywords): return True
    context_patterns = [r'study\s+(in|at)\s+\w+', r'(fund|funding|support)\s+(for|to)\s+(study|education|university)', r'(graduate|master.?s)\s+(in|at)\s+\w+',]
    if any(re.search(pattern, lower_case_input) for pattern in context_patterns): return True
    return False

# --- Model and Persona Configuration ---
persona_instruction = (
    "You are 'ScholarBot', a professional and encouraging AI expert for Pakistani students seeking Master's scholarships abroad. "
    "Your tone should be helpful, clear, and formal but friendly. "
    "When a conversation starts, greet the user warmly (e.g., 'Assalamu alaikum!' or 'Hello!'). In subsequent turns, DO NOT repeat the greeting; get straight to the point. "
    "Format your responses clearly using Markdown. Use lists and bold text for key terms. "
    "If the user asks about unrelated topics, you MUST politely decline and redirect them back to the topic of scholarships. "
)

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=persona_instruction)

if "chat" not in st.session_state:
    chat_history_for_api = [genai.types.Content(role=msg["role"], parts=[genai.types.Part(text=msg["content"])]) for msg in st.session_state.get("messages", [])]
    st.session_state.chat = model.start_chat(history=chat_history_for_api)

def stream_to_string_generator(stream):
    for chunk in stream:
        if chunk.text: yield chunk.text

# --- Streamlit UI ---

# <-- NEW: Image Uploader moved to the top of the main page in an expander.
with st.expander("📎 Attach an Image (Optional)"):
    uploaded_file = st.file_uploader(
        "Upload a relevant image to discuss.",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed" # Hides the default label for a cleaner look
    )
    if uploaded_file:
        st.image(uploaded_file, caption="Your image will be sent with your next message.")

st.title("ScholarBot")
status_placeholder = st.empty()
status_placeholder.text("Ready")

# --- Sidebar with Control Features ---
with st.sidebar:
    st.header("About This Project")
    st.markdown("**ScholarBot** is an AI-powered chatbot designed to provide Pakistani students with initial information about Master's scholarship opportunities.")
    st.divider()

    if st.button("✨ New Chat"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

    st.divider()
    st.header("Example Prompts")
    example_prompts = [
        "What scholarships are available in the UK?",
        "Compare the Fulbright and Chevening scholarships.",
        "How do I write a good Statement of Purpose?",
    ]
    for prompt_text in example_prompts:
        if st.button(prompt_text):
            st.session_state.user_input = prompt_text
            st.rerun()
    # <-- The image uploader section has been REMOVED from the sidebar.

# --- Chat History Display ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am ScholarBot. Ask me about Master's scholarships abroad for Pakistani students."}]

for message in st.session_state.messages:
    avatar_icon = logo_image if message["role"] == "assistant" else "👤"
    with st.chat_message(name=message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# --- Main Logic: Handle User Input ---
prompt = None
if st.session_state.get("user_input"):
    prompt = st.session_state.user_input
    del st.session_state.user_input
elif chat_input := st.chat_input("Ask about scholarships..."):
    prompt = chat_input

if prompt:
    if len(prompt) > 2000:
        st.error("Your message is too long. Please keep your query under 2000 characters.")
        st.stop()

    user_message_content = prompt
    image_to_send = None
    if uploaded_file:
        user_message_content += f"\n*(Image Attached: {uploaded_file.name})*"
        image_to_send = Image.open(uploaded_file)

    st.session_state.messages.append({"role": "user", "content": user_message_content})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_message_content)

    assistant_response = None
    lower_case_prompt = prompt.lower()
    if not image_to_send:
        if lower_case_prompt in faqs:
            assistant_response = faqs[lower_case_prompt]
        elif not is_scholarship_query(prompt):
            assistant_response = "I’m ScholarBot, here to help with Master’s scholarships! Please ask about scholarships, funding, or studying abroad (e.g., 'scholarships in Germany')."

    if assistant_response:
        with st.chat_message("assistant", avatar=logo_image):
            st.markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    else:
        api_prompt_parts = [prompt] if prompt else []
        if image_to_send: api_prompt_parts.append(image_to_send)
        with st.chat_message("assistant", avatar=logo_image):
            status_placeholder.text("Thinking...")
            try:
                response_stream = st.session_state.chat.send_message(api_prompt_parts, stream=True)
                string_generator = stream_to_string_generator(response_stream)
                full_response = st.write_stream(string_generator)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                print(f"AN ERROR OCCURRED: {e}")
                error_message = "Sorry, I've run into a technical issue. Please try your question again in a moment."
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
            finally:
                status_placeholder.text("Ready")