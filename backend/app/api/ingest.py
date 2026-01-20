from fastapi import APIRouter, UploadFile, File
from pathlib import Path
from services.ocr import extract_text
from services.embedding import compute_embeddings
from services.vectorstore import store_chunks

router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/document")
async def upload_document(file: UploadFile = File(...)):
    # Save file
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text (OCR if needed)
    text = extract_text(file_path)

    # Chunk text
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]

    # Compute embeddings
    embeddings = compute_embeddings(chunks)

    # Store chunks + embeddings in FAISS (or local vectorstore)
    store_chunks(chunks, embeddings, file.filename)

    return {"filename": file.filename, "chunks": len(chunks)}
