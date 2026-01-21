# backend/services/vectorstore.py
from pathlib import Path
import pickle

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

VECTOR_DB = DATA_DIR / "vectorstore.pkl"

def _load_store():
    if VECTOR_DB.exists():
        with open(VECTOR_DB, "rb") as f:
            return pickle.load(f)
    return {}

def _save_store(store):
    with open(VECTOR_DB, "wb") as f:
        pickle.dump(store, f)

def store_chunks(chunks, embeddings, doc_id):
    store = _load_store()
    store[doc_id] = [
        {"chunk": c, "embedding": e}
        for c, e in zip(chunks, embeddings)
    ]
    _save_store(store)

def load_chunks():
    return _load_store()
