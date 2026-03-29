import faiss
import numpy as np
import pickle
import re
from sentence_transformers import SentenceTransformer

# --- CONFIGURATION ---
DATA_FILE = "club_data.txt"
INDEX_FILE = "faiss_index.bin"
CHUNKS_FILE = "chunks.pkl"
EMBEDDINGS_FILE = "embeddings.npy"

# --- 1. CLEANING FUNCTION (Keep Newlines) ---
def clean_text(text):
    # Replace tabs/multiple spaces with single space
    text = re.sub(r'[ \t]+', ' ', text)
    # Remove awkward spacing before punctuation
    text = re.sub(r'\s+([?.!,])', r'\1', text)
    # Ensure paragraphs are separated by exactly two newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# --- 2. CHUNKING FUNCTION (Character-based with Overlap) ---
def chunk_text(text, chunk_size=800, overlap=200):
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size
        
        # If we aren't at the end, try to find a nice break point (newline or space)
        if end < text_len:
            # Look for the last newline in the current window
            cut_point = text.rfind('\n', start, end)
            if cut_point == -1:
                # If no newline, look for the last space
                cut_point = text.rfind(' ', start, end)
            
            # If we found a good spot, cut there
            if cut_point != -1:
                end = cut_point
        
        # Grab the chunk
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move the window forward, backing up by 'overlap' to capture context
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
    # 800 characters is safe for the MiniLM model (approx 200 tokens)
    chunks = chunk_text(cleaned_text, chunk_size=800, overlap=200)
    
    print(f"✅ Created {len(chunks)} chunks.")
    if len(chunks) > 0:
        print(f"   Preview Chunk 1: {chunks[0][:100]}...")

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

    print("🎉 SUCCESS: Index rebuilt! You can now run 'streamlit run app.py'")

if __name__ == "__main__":
    build()