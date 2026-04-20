from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.routes.query import router
from app.services.file_parser import extract_text_from_pdf, extract_text_from_image

app = FastAPI(title="Intellora AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.filename.endswith(".pdf"):
        content = await file.read()
        text = extract_text_from_pdf(content)
    else:
        content = await file.read()
        text = extract_text_from_image(content)

    return {"text": text}

@app.get("/")
def home():
    return {"message": "🚀 Intellora API is live"}