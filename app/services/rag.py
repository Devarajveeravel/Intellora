# SIMPLE WORKING RAG (NO TORCH, NO ERRORS)

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
        score = sum(word.lower() in chunk.lower() for word in query.split())
        scored.append((score, chunk))

    scored.sort(reverse=True)

    return "\n".join([c for _, c in scored[:top_k]])