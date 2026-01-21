# backend/app/api/ingest.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil

# Create FastAPI router
router = APIRouter()

# Directory to store uploaded PDFs
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/document", summary="Upload a PDF document")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF file, save it locally, and return the path.
    """
    # Only allow PDF files
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # Define file path
    file_path = UPLOAD_DIR / file.filename

    # Save file safely
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")
    finally:
        file.file.close()

    return {
        "filename": file.filename,
        "path": str(file_path),
        "message": "File uploaded successfully."
    }
