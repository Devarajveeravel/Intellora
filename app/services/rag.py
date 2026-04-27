from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

chunks = []
embeddings = None


# 🔥 SPLIT PDF INTO CHUNKS
def split_text(text, chunk_size=300):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]


# 🔥 STORE DOCUMENT
def ingest_document(text):
    global chunks, embeddings

    chunks = split_text(text)

    if not chunks:
        return

    embeddings = model.encode(chunks)


# 🔥 RETRIEVE BEST CONTEXT
def retrieve_context(query, top_k=3):
    global embeddings, chunks

    if embeddings is None:
        return ""

    query_embedding = model.encode([query])[0]

    scores = np.dot(embeddings, query_embedding)

    top_indices = np.argsort(scores)[-top_k:][::-1]

    return "\n".join([chunks[i] for i in top_indices])