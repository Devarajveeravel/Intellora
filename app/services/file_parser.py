import PyPDF2

def extract_text_from_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""

        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"

        print("EXTRACTED TEXT LENGTH:", len(text))

        return text

    except Exception as e:
        print("PDF ERROR:", e)
        return ""