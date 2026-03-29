import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

INDEX_FILE = "faiss_index.bin"
CHUNKS_FILE = "chunks.pkl"

class Retriever:
    def __init__(self, model_name="all-MiniLM-L6-v2", top_k=3):
        self.top_k = top_k

        # Load model
        self.model = SentenceTransformer(model_name)

        # Auto-build index if files are missing (e.g. on Streamlit Cloud)
        if not os.path.exists(INDEX_FILE) or not os.path.exists(CHUNKS_FILE):
            print("⚠️ Index files not found. Building index from VIT_data.txt...")
            from build_index import build
            build()
            print("✅ Index built successfully.")

        # Load FAISS index
        print("🔹 Loading FAISS index...")
        self.index = faiss.read_index(INDEX_FILE)

        # Load chunks
        print("🔹 Loading text chunks...")
        with open(CHUNKS_FILE, "rb") as f:
            self.chunks = pickle.load(f)

        print(f"✅ Retriever ready — {len(self.chunks)} chunks loaded.")

    def retrieve(self, query):
        query_vec = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_vec, self.top_k)

        results = []
        for idx in indices[0]:
            results.append(self.chunks[idx])

        return results
