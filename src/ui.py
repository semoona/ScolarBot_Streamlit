# src/ui.py
import streamlit as st

def load_css():
    """Injects custom CSS for styling the app."""
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

def render_sidebar():
    """Renders the sidebar with its control features."""
    with st.sidebar:
        st.header("About This Project")
        st.markdown("**ScholarBot** is an AI-powered chatbot designed to provide Pakistani students with initial information about Master's scholarship opportunities.")
        st.divider()

        if st.button("✨ New Chat", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        st.divider()
        st.header("📎 Attach an Image")
        uploaded_file = st.file_uploader(
            "Upload an image to discuss with the bot.",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed"
        )
        if uploaded_file:
            st.image(uploaded_file)

        st.divider()
        st.header("Example Prompts")
        example_prompts = [
            "What scholarships are available in the UK?",
            "Compare the Fulbright and Chevening scholarships.",
            "How do I write a good Statement of Purpose?",
        ]
        for prompt_text in example_prompts:
            if st.button(prompt_text, use_container_width=True):
                st.session_state.new_prompt = prompt_text
                st.rerun()
                
    return uploaded_file