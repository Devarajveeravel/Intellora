import PyPDF2

def extract_text_from_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        # 🔥 CLEAN TEXT
        text = text.strip()

        if not text:
            return "No readable text found in PDF."

        return text[:8000]  # limit size

    except Exception as e:
        print("PDF ERROR:", e)
        return "Error reading PDF"