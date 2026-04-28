from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.file_parser import extract_text
from app.services.rag import ingest_document, retrieve_context
import os
from groq import Groq

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# GROQ CLIENT
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# REQUEST MODEL
class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"
    file_text: str = ""


# ✅ QUERY API
@app.post("/query")
def query_api(data: QueryRequest):
    query = data.query
    file_text = data.file_text

    # 🔥 RAG LOGIC
    context = ""
    if file_text:
        ingest_document(file_text)
        context = retrieve_context(query)

    prompt = f"""
Answer in clean bullet points.
If code is asked → give proper formatted code block.

Context:
{context}

Question:
{query}
"""

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"answer": completion.choices[0].message.content}


# ✅ PDF UPLOAD API
@app.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    text = extract_text(file.file)
    return {"text": text}