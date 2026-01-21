# backend/app/api/qa.py
from fastapi import APIRouter
from pydantic import BaseModel
from services.vectorstore import load_chunks

router = APIRouter()

class QARequest(BaseModel):
    question: str
    doc_id: str

@router.post("/")
def ask_question(payload: QARequest):
    store = load_chunks()

    if payload.doc_id not in store:
        return {"answer": "Document not found", "source": None}

    top_chunk = store[payload.doc_id][0]["chunk"]
    return {
        "answer": top_chunk[:300] + "...",
        "source": payload.doc_id
    }
