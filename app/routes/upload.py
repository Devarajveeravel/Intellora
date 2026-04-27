from fastapi import APIRouter, UploadFile, File
from app.services.file_parser import extract_text_from_pdf

router = APIRouter()

@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        text = extract_text_from_pdf(file.file)

        return {
            "message": "PDF uploaded successfully",
            "text": text   # 🔥 IMPORTANT
        }

    except Exception as e:
        print("UPLOAD ERROR:", e)
        return {
            "message": "Upload failed",
            "text": ""
        }