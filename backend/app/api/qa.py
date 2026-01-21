from fastapi import APIRouter
from services.vectorstore import load_chunks

router = APIRouter()

@router.post("/")
def ask_question(question: str, doc_id: str):
    store = load_chunks()
    if doc_id not in store:
        return {"answer": "Document not found", "source": None}

    top_chunk = store[doc_id][0]
    return {"answer": top_chunk["chunk"][:200] + "...", "source": doc_id}
