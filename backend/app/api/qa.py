from pathlib import Path
import pickle

VECTOR_DB = Path("data/vectorstore.pkl")

store = {}  # In-memory store

def store_chunks(chunks, embeddings, doc_id):
    """
    Store chunks and embeddings in memory or persist to file.
    """
    global store
    store[doc_id] = [{"chunk": c, "embedding": e} for c, e in zip(chunks, embeddings)]
    # Persist to disk
    with open(VECTOR_DB, "wb") as f:
        pickle.dump(store, f)

def load_chunks():
    global store
    if VECTOR_DB.exists():
        import pickle
        with open(VECTOR_DB, "rb") as f:
            store = pickle.load(f)
    return store
