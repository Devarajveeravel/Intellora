import os
from pypdf import PdfReader
from app.services.retriever import add_documents

DATA_PATH = "data"

# 🔥 Chunking function
def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))

    return chunks


def load_pdfs():
    documents = []

    for file in os.listdir(DATA_PATH):
        if file.endswith(".pdf"):
            file_path = os.path.join(DATA_PATH, file)

            try:
                reader = PdfReader(file_path)

                for page in reader.pages:
                    try:
                        text = page.extract_text()
                        if text:
                            # 🔥 APPLY CHUNKING HERE
                            chunks = chunk_text(text)
                            documents.extend(chunks)

                    except Exception:
                        print(f"⚠️ Skipping bad page in {file}")

            except Exception:
                print(f"❌ Failed to read {file}, skipping...")

    return documents


def ingest_documents():
    docs = load_pdfs()

    if docs:
        add_documents(docs)
        print(f"✅ {len(docs)} chunks ingested successfully!")
    else:
        print("⚠️ No valid documents found.")