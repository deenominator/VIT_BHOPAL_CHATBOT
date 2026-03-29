# VIT Bhopal Information Chatbot

> A RAG-powered chatbot for VIT Bhopal University — built with FAISS, Sentence Transformers, and OpenRouter API, deployed on Streamlit.

## Deployed Link: https://vitbhopalchatbot.streamlit.app/
---

## Overview

The VIT Bhopal Information Chatbot answers questions about VIT Bhopal University using **Retrieval-Augmented Generation (RAG)**. It retrieves relevant chunks from a local knowledge base and sends them to an LLM via the OpenRouter API to generate accurate, context-aware responses.

It supports two user roles — **students** and **general public** — with a personalized onboarding flow and a built-in support ticket system.

---

## Features

- **RAG Pipeline** — FAISS vector search over a curated university knowledge base
- **LLM-powered answers** — via OpenRouter API (model-agnostic)
- **Role-based experience** — separate flows for students and visitors
- **Ticket system** — automatically creates support tickets for help/issue queries
- **Auto index building** — index is built on first run if missing (Streamlit Cloud ready)
- **Clean UI** — custom styled chat interface built with Streamlit

---

## Project Structure

```
vit_bhopal_chatbot/
│
├── app.py               # Main Streamlit app — UI, routing, chat logic
├── build_index.py       # Builds FAISS index from VIT_data.txt
├── retriever.py         # Loads FAISS index & retrieves relevant chunks
├── client.py            # Calls OpenRouter LLM API
├── ticket_system.py     # Creates and manages support tickets
├── utils.py             # Helper utilities
├── VIT_data.txt         # University knowledge base (plain text)
├── requirements.txt     # Python dependencies
├── logo.png             # App logo
│
├── faiss_index.bin      # Generated — not in repo (auto-built on startup)
├── chunks.pkl           # Generated — not in repo (auto-built on startup)
└── embeddings.npy       # Generated — not in repo (auto-built on startup)
```

---

## How It Works

```
User Query
    │
    ▼
Sentence Transformer (all-MiniLM-L6-v2)
    │  encodes query into a vector
    ▼
FAISS Index
    │  finds top-3 most relevant text chunks from VIT_data.txt
    ▼
OpenRouter LLM API
    │  receives chunks + query, generates a response
    ▼
Streamlit Chat UI
```

On **first startup** (e.g. on Streamlit Cloud), if `faiss_index.bin` or `chunks.pkl` are missing, `retriever.py` automatically calls `build_index.py` to generate them from `VIT_data.txt`.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/vit_bhopal_chatbot.git
cd vit_bhopal_chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API key

Create a `.env` file in the root directory:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 4. Build the FAISS index (first time only)

```bash
python build_index.py
```

This reads `VIT_data.txt`, creates text chunks, generates embeddings, and saves `faiss_index.bin` and `chunks.pkl`.

### 5. Run the app

```bash
streamlit run app.py
```

---

## Deploying to Streamlit Cloud

1. Push all files to GitHub — **do not push** `faiss_index.bin`, `chunks.pkl`, or `embeddings.npy` (these are auto-generated)
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) and connect your repo
3. Add your `OPENROUTER_API_KEY` under **Settings → Secrets**:
   ```toml
   OPENROUTER_API_KEY = "your_key_here"
   ```
4. Deploy — the index will be built automatically on first startup

---

## Requirements

Key dependencies (see `requirements.txt` for full list):

| Package | Purpose |
|---|---|
| `streamlit` | Web app framework |
| `faiss-cpu` | Vector similarity search |
| `sentence-transformers` | Text embeddings (MiniLM) |
| `openai` / `requests` | OpenRouter API calls |
| `numpy` | Embedding matrix operations |
| `pickle` | Chunk serialization |

---

## Knowledge Base

The chatbot's knowledge comes from `VIT_data.txt`, a curated document covering:

- University overview, vision & mission
- Academic programs and curriculum
- Campus facilities and infrastructure
- Placements and industry connections
- Student clubs and events
- Scholarships and global opportunities

To update the knowledge base, edit `VIT_data.txt` and re-run `python build_index.py`.

---

## Ticket System

If a user's message contains keywords like `help`, `issue`, `problem`, `support`, or `not working`, the bot automatically creates a support ticket instead of querying the LLM, and returns a ticket ID to the user.

---

## User Roles

| Role | Flow |
|---|---|
| **General Visitor** | Direct welcome message → chat |
| **Student** | Optional name + branch input → personalized welcome → chat |

Users can switch roles anytime using **"Start Over / Change Role"** in the sidebar.

---
