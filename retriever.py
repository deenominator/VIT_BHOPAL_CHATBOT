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

        # Load FAISS index
        print("🔹 Loading FAISS index...")
        self.index = faiss.read_index(INDEX_FILE)

        # Load chunks
        print("🔹 Loading text chunks...")
        with open(CHUNKS_FILE, "rb") as f:
            self.chunks = pickle.load(f)

        print(f"Retriever ready — {len(self.chunks)} chunks loaded.")

    def retrieve(self, query):
        """
        Embeds a user query, performs FAISS search, 
        and returns the most relevant text chunks.
        """
        query_vec = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_vec, self.top_k)

        results = []
        for idx in indices[0]:
            results.append(self.chunks[idx])

        return results
