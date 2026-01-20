def extract_text(file_path):
    """
    Stub: for now, just read PDF text using PyPDF2.
    Later you can add Tesseract OCR for scanned PDFs.
    """
    import PyPDF2

    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text
