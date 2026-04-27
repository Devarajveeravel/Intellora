from fastapi import APIRouter, UploadFile, File
from app.services.file_parser import extract_text_from_pdf
from app.services.rag import ingest_document

router = APIRouter()

@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file.file)

    # 🔥 THIS LINE FIXES YOUR WHOLE PROBLEM
    ingest_document(text)

    return {
        "message": "PDF uploaded successfully",
        "text": text[:5000]   # frontend needs this
    }