import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# --- API KEY SETUP ---
try:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
except:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    st.error("❌ API Key not found! Add it to Streamlit Secrets.")
    st.stop()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def call_llm(context_chunks, user_query):
    """
    Sends the RAG context + user query to OpenRouter LLM.
    """
    context = "\n\n".join(context_chunks)

    # --- THE FIX IS IN THIS PROMPT ---
    prompt = f"""
 You are VIT Bhopal InfoBot, a helpful assistant for students and staff at VIT Bhopal.
 Use ONLY the information in the context below to answer.

 FORMATTING RULES:
 1. If listing items (like events or teams), use Bullet Points.
 2. Use **Bold** for specific names, dates, or titles.
 3. Do not squish everything into one paragraph.

 CONTEXT:
 {context}

 USER QUESTION:
 {user_query}

 ANSWER:
 """

    payload = {
        "model": "google/gemma-2-9b-it",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Follow formatting rules strictly."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3 # Slightly higher creativity for better formatting
    }

    try:
        response = requests.post(OPENROUTER_URL, json=payload, headers=HEADERS)
        if response.status_code != 200:
            return f"Error: {response.text}"
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error connecting to LLM: {str(e)}"