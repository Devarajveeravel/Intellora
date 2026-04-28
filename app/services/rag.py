chunks = []

def ingest_document(text):
    global chunks
    words = text.split()
    chunks = [" ".join(words[i:i+300]) for i in range(0, len(words), 300)]

def retrieve_context(query, top_k=3):
    global chunks

    if not chunks:
        return ""

    # 🔥 simple fallback (no embeddings)
    return "\n".join(chunks[:top_k])