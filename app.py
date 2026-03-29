import streamlit as st
from client import call_llm
from retriever import Retriever
from ticket_system import TicketSystem
import base64
def set_membership():
    choice = st.session_state.member_choice

    if choice == "No, I'm not a student":
        st.session_state.membership = False
        st.session_state.public_intro_done = False

    elif choice == "Yes, I'm a student":
        st.session_state.membership = True
        st.session_state.student_intro_done = False


st.set_page_config(page_title="VIT Bhopal Info Chatbot", page_icon="logo.png", layout="centered")


# -------------------------------  
# CSS  
# -------------------------------
def add_css():
    st.markdown("""
        <style>
            .chat-container {
                max-height: 500px;
                overflow-y: auto;
                padding: 10px;
                border-radius: 10px;
              }
            body { background-color: #0d0d0d; }

            .header-title {
                text-align: center;
                font-size: 40px;
                font-weight: 700;
                color: white;
                margin-top: -10px;
            }

            .subtitle {
                text-align: center;
                font-size: 16px;
                color: #bbbbbb;
                margin-bottom: 25px;
            }

            .bot-message {
                background-color: #1e1e1e;
                padding: 15px;
                border-radius: 12px;
                margin-bottom: 10px;
                color: white;
                border-left: 4px solid #4285F4;
            }

            .user-message {
                background-color: #2b2b2b;
                padding: 15px;
                border-radius: 12px;
                margin-bottom: 10px;
                color: white;
                text-align: right;
                border-right: 4px solid #34A853;
            }

            .center-img {
                display: flex;
                justify-content: center;
                margin-bottom: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

def load_logo():
    try:
        with open("logo.png", "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
            st.markdown(
                f"<div class='center-img'><img src='data:image/png;base64,{encoded}' width='130'></div>",
                unsafe_allow_html=True
            )
    except:
        pass

add_css()
load_logo()

# -------------------------------
# SIDEBAR - RESET BUTTON
# -------------------------------
with st.sidebar:
    st.write("### Options")
    
    # This button resets the app state
    if st.button("Start Over / Change Role"):
        for key in ["membership", "student_intro_done", "public_intro_done", "messages", "name", "branch"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
# -------------------------------
# Header
# -------------------------------
st.markdown("<div class='header-title'>VIT Bhopal Information Chatbot</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Powered by RAG + OpenRouter API</div>", unsafe_allow_html=True)

# -------------------------------
# Session State
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "membership" not in st.session_state:
    st.session_state.membership = None

if "name" not in st.session_state:
    st.session_state.name = ""

if "team" not in st.session_state:
    st.session_state.team = ""

if "student_intro_done" not in st.session_state:
    st.session_state.student_intro_done = False

if "public_intro_done" not in st.session_state:
    st.session_state.public_intro_done = False

# Load tools
retriever = Retriever()
ticket_system = TicketSystem()

if st.session_state.membership is None:

    st.radio(
        "Are you a Student at the university?",
        ["Select", "No, I'm not a student", "Yes, I'm a student"],
        index=0,
        key="member_choice",
        on_change=set_membership   
    )

    st.stop()

# -------------------------------
# FIXED — STEP 2 — NON-MEMBER INTRO
# -------------------------------
if st.session_state.membership is False and not st.session_state.public_intro_done:

    intro = (
        "✨ **Welcome to VIT Bhopal!**\n\n"
        "Feel free to ask me anything about the university"
    )

    st.session_state.messages.append({"role": "assistant", "content": intro})
    st.session_state.public_intro_done = True

# -------------------------------
# FIXED — STEP 2 — MEMBER DETAILS (OPTIONAL)
# -------------------------------
if st.session_state.membership is True and not st.session_state.student_intro_done:

    st.markdown("### Student Details (Optional)")

    name = st.text_input("Your name:", key="student_name")
    branch = [
        "AIML", "CORE", "Health Informatics", "Education Technology",
        "Cybersecurity", "Bioengineering", "Aerospace", "Robotics"
    ]
    team = st.selectbox("Your branch:", [""] + branch, key="student_branch")

   # Create two columns for buttons
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # BACK BUTTON
        if st.button("⬅ Back"):
            st.session_state.membership = None # Reset choice
            st.rerun()

    with col2:
        # CONTINUE BUTTON
        if st.button("Continue", key="student_continue"):
            st.session_state.name = name
            st.session_state.team = team

            # Personalized intro
            if name:
                intro = f"Hi {name}! 👋 Great to have someone from the **{branch} Branch**!"
            else:
                intro = "Welcome Student! 👋 How can I assist you today?"

            st.session_state.messages.append({"role": "assistant", "content": intro})
            st.session_state.student_intro_done = True
            st.rerun()

    st.stop()

# -------------------------------
# CHAT SECTION — FIXED LAYOUT
# -------------------------------

chat_container = st.container()   
with chat_container:
    
    # Show previous messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-message'>{msg['content']}</div>", unsafe_allow_html=True)

    # Input stays BOTTOM of chat
  # Define a function to handle the submission
def process_input():
    user_input = st.session_state.chat_input
    if user_input:
        # 1. Append User Message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # 2. Process Logic
        help_keywords = ["help", "issue", "problem", "support", "not working", "raise a ticket"]
        if any(k in user_input.lower() for k in help_keywords):
            ticket_id = ticket_system.create_ticket(user_input)
            reply = f"📝 Ticket created! ID: **{ticket_id}**."
        else:
            chunks = retriever.retrieve(user_input)
            with st.expander("🕵️ Debug: What the bot is reading"):
              for i, chunk in enumerate(chunks):
                st.write(f"**Chunk {i+1}:** {chunk}")
            reply = call_llm(chunks, user_input)

        # 3. Append Bot Reply
        st.session_state.messages.append({"role": "assistant", "content": reply})

        # 4. Clear the input (Allowed here because it's inside a callback)
        st.session_state.chat_input = ""

# Link the function to the widget using 'on_change'
st.text_input("Ask me anything about VIT Bhopal University...", key="chat_input", on_change=process_input)