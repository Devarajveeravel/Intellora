from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.file_parser import extract_text
from app.services.rag import ingest_document, retrieve_context
from app.services.llm import generate_llm_answer  # ✅ IMPORTANT

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


# ✅ QUERY API (FINAL FIXED)
@app.post("/query")
def query_api(data: QueryRequest):
    query = data.query
    file_text = data.file_text

    context = ""
    if file_text:
        ingest_document(file_text)
        context = retrieve_context(query)

    # 🔥 USE LLM FILE (THIS FIXES YOUR ISSUE)
    answer = generate_llm_answer(query, context)

    return {"answer": answer}


# ✅ PDF UPLOAD
@app.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    text = extract_text(file.file)
    return {"text": text}


# ✅ HEALTH CHECK (IMPORTANT FOR RENDER)
@app.get("/")
def home():
    return {"message": "Intellora Backend Running 🚀"}