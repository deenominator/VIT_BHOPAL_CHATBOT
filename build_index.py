import faiss
import numpy as np
import pickle
import re
from sentence_transformers import SentenceTransformer

# --- CONFIGURATION ---
DATA_FILE = "VIT_data.txt"
INDEX_FILE = "faiss_index.bin"
CHUNKS_FILE = "chunks.pkl"
EMBEDDINGS_FILE = "embeddings.npy"

# --- 1. CLEANING FUNCTION (Keep Newlines) ---
def clean_text(text):
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\s+([?.!,])', r'\1', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# --- 2. CHUNKING FUNCTION (Character-based with Overlap) ---
def chunk_text(text, chunk_size=800, overlap=200):
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size
        if end < text_len:
            cut_point = text.rfind('\n', start, end)
            if cut_point == -1:
                cut_point = text.rfind(' ', start, end)
            if cut_point != -1:
                end = cut_point
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap

    return chunks

# --- 3. MAIN BUILD SCRIPT ---
def build():
    print("🔹 Loading document...")
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        raw_text = f.read()

    print("🔹 Cleaning text...")
    cleaned_text = clean_text(raw_text)

    print("🔹 Chunking text...")
    chunks = chunk_text(cleaned_text, chunk_size=800, overlap=200)
    print(f"✅ Created {len(chunks)} chunks.")

    print("🔹 Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("🔹 Creating embeddings...")
    embeddings = model.encode(chunks, convert_to_numpy=True, show_progress_bar=True)

    print("🔹 Building FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    print("🔹 Saving files...")
    faiss.write_index(index, INDEX_FILE)
    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(chunks, f)
    np.save(EMBEDDINGS_FILE, embeddings)

    print("🎉 Index built successfully!")

if __name__ == "__main__":
    build()
