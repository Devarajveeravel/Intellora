from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.file_parser import extract_text
from app.services.rag import ingest_document, retrieve_context
from app.services.llm import generate_llm_answer
import re

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ REQUEST MODEL
class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"
    file_text: str = ""


# 🔥 FINAL FORMAT ENFORCER (MAIN FIX)
def force_final_format(text: str):
    import re

    # clean text
    text = text.replace("•", " ").replace("-", " ")
    text = re.sub(r"\s+", " ", text).strip()

    # split into sentences OR chunks
    sentences = re.split(r'(?<=[.!?])\s+', text)

    lines = []
    for s in sentences:
        s = s.strip()
        if s:
            lines.append(s)

    # 🔥 CRITICAL: double newline for markdown
    return "\n\n".join(lines)


# ✅ QUERY API (FINAL FIXED)
@app.post("/query")
def query_api(data: QueryRequest):
    query = data.query
    file_text = data.file_text

    context = ""
    if file_text:
        ingest_document(file_text)
        context = retrieve_context(query)

    # 🔥 GET RAW LLM RESPONSE
    raw_answer = generate_llm_answer(query, context)

    # 🔥 FORCE STRUCTURE HERE (ULTIMATE FIX)
    final_answer = force_final_format(raw_answer)

    return {"answer": final_answer}


# ✅ PDF UPLOAD
@app.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    text = extract_text(file.file)
    return {"text": text}


# ✅ ROOT (RENDER HEALTH CHECK)
@app.get("/")
def home():
    return {"message": "Intellora Backend Running 🚀"}