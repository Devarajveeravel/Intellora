from fastapi import APIRouter, UploadFile, File
from app.services.file_parser import extract_text_from_pdf

router = APIRouter()

uploaded_text_store = {}

@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file.file)

    if not text:
        return {"text": "", "message": "Failed to read PDF"}

    # store full text
    uploaded_text_store["text"] = text[:10000]

    return {
        "text": uploaded_text_store["text"],
        "message": "PDF uploaded successfully"
    }