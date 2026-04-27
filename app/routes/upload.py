from fastapi import APIRouter, UploadFile, File
from app.services.file_parser import extract_text_from_pdf
import base64

router = APIRouter()

# ✅ Global storage
uploaded_data = {
    "pdf": "",
    "image": ""
}

@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file.file)

    # ✅ store text (limit size)
    uploaded_data["pdf"] = text[:8000]

    return {
        "message": "PDF uploaded successfully",
        "text": uploaded_data["pdf"]
    }


@router.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    content = await file.read()
    encoded = base64.b64encode(content).decode("utf-8")

    uploaded_data["image"] = encoded

    return {
        "message": "Image uploaded successfully"
    }