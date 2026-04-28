# SIMPLE RAG (NO HEAVY LIBS)

chunks = []

def split_text(text, chunk_size=300):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def ingest_document(text):
    global chunks
    chunks = split_text(text)

def retrieve_context(query, top_k=3):
    global chunks

    if not chunks:
        return ""

    scored = []

    for chunk in chunks:
        score = sum(1 for word in query.lower().split() if word in chunk.lower())
        scored.append((score, chunk))

    scored.sort(reverse=True)

    return "\n".join([c for _, c in scored[:top_k]])