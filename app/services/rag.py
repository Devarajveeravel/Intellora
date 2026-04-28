chunks = []
embeddings = []


def split_text(text, size=300):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]


def ingest_document(text):
    global chunks
    chunks = split_text(text)


def retrieve_context(query, top_k=3):
    if not chunks:
        return ""

    return "\n".join(chunks[:top_k])