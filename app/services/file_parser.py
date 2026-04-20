import PyPDF2

# ✅ PDF WORKS
def extract_text_from_pdf(file_bytes):
    try:
        reader = PyPDF2.PdfReader(file_bytes)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return "Error reading PDF"


def extract_text_from_image(file_bytes):
    return "⚠️ Image OCR not supported in live version"