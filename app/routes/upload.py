from fastapi import APIRouter, UploadFile, File
from app.services.file_parser import extract_text_from_pdf

router = APIRouter()

@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file.file)

    return {
        "text": text[:8000]  # send usable context
    }