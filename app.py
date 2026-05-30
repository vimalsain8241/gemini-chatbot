import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Streamlit page settings
st.set_page_config(
    page_title="Laxman k papa ka Chatbot",
    page_icon="🧟",
    layout="wide"
)

# Get API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not found in .env file")
    st.stop()

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Load model
model = genai.GenerativeModel("gemini-2.5-flash")

# Create chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Title
st.title("🧟 Laxman k papa ka Chatbot")

# Display chat history
for message in st.session_state.chat_session.history:

    role = "assistant" if message.role == "model" else "user"

    with st.chat_message(role):
        try:
            st.markdown(message.parts[0].text)
        except:
            pass

# User input
user_prompt = st.chat_input("Ask me anything...")

if user_prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    try:
        # Send to Gemini
        response = st.session_state.chat_session.send_message(
            user_prompt
        )

        # Display Gemini response
        with st.chat_message("assistant"):
            st.markdown(response.text)

    except Exception as e:
        st.error(f"Error: {e}")