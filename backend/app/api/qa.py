# backend/app/api/qa.py
from fastapi import APIRouter
from pydantic import BaseModel
from services.vectorstore import load_chunks

router = APIRouter()

# Define request body
class QARequest(BaseModel):
    question: str
    doc_id: str

@router.post("/")
def ask_question(request: QARequest):
    """
    Answer a question based on the uploaded document.
    """
    store = load_chunks()
    doc_id = request.doc_id

    if doc_id not in store:
        return {"answer": "Document not found", "source": None}

    # Simple RAG: return first chunk as answer
    top_chunk = store[doc_id][0]
    return {
        "answer": top_chunk["chunk"][:200] + "...",  # truncate for preview
        "source": doc_id
    }
