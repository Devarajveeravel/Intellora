import PyPDF2

def extract_text_from_pdf(file_bytes):
    try:
        reader = PyPDF2.PdfReader(file_bytes)
        text = ""

        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"

        return text.strip()

    except Exception as e:
        print("PDF ERROR:", e)
        return ""