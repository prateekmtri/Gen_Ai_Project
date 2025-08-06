from PyPDF2 import PdfReader
from io import BytesIO

def extract_text_from_pdf(file_bytes: bytes) -> str:
    file_stream = BytesIO(file_bytes)
    reader = PdfReader(file_stream)

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    return text
