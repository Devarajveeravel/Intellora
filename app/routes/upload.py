from fastapi import APIRouter, UploadFile, File
from app.services.file_parser import extract_text_from_pdf
import base64

router = APIRouter()

uploaded_data = {
    "pdf": "",
    "image": ""
}

@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file.file)
    uploaded_data["pdf"] = text[:5000]

    return {"message": "PDF uploaded successfully"}

@router.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    content = await file.read()
    encoded = base64.b64encode(content).decode("utf-8")

    uploaded_data["image"] = encoded

    return {"message": "Image uploaded successfully"}