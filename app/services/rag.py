from sentence_transformers import SentenceTransformer
import numpy as np

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Dummy in-memory store (replace with vector DB later)
documents = [
    "Artificial Intelligence is the simulation of human intelligence by machines.",
    "Machine Learning is a subset of AI that learns from data.",
    "Deep Learning uses neural networks with many layers."
]

doc_embeddings = model.encode(documents)


def get_rag_answer(query: str):
    try:
        query_embedding = model.encode([query])[0]

        # Compute similarity
        similarities = np.dot(doc_embeddings, query_embedding)

        # Get best match
        best_idx = np.argmax(similarities)

        return documents[best_idx]

    except Exception:
        return ""