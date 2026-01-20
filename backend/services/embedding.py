def compute_embeddings(chunks):
    """
    Stub embedding: use sentence-transformers or dummy vectors.
    For MVP without OpenAI, we return random vectors.
    """
    import numpy as np
    embeddings = [np.random.rand(384).tolist() for _ in chunks]  # 384-dim fake vector
    return embeddings
