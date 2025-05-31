import fitz  # PyMuPDF

def extract_text_from_pdf(file):
    # file is a file-like object (e.g., from Streamlit)
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text
