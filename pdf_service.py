import io
from pypdf import PdfReader
from fastapi import UploadFile


async def extract_text_from_pdf(file: UploadFile) -> str:
    """Read PDF content from an uploaded file and return extracted text."""
    content = await file.read()
    reader = PdfReader(io.BytesIO(content))
    text_chunks = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        text_chunks.append(page_text)

    return "\n".join(text_chunks).strip()
