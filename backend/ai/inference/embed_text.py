"""
Inference module for generating embeddings using trained TVET model
This integrates with the RAG pipeline for semantic search
"""

import logging
from pathlib import Path
from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TVETEmbedder:
    """Generate embeddings using TVET-trained model"""
    
    _instance = None  # Singleton pattern
    
    def __new__(cls, model_path: str = "models/tvet-embeddings"):
        """Ensure single model instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, model_path: str = "models/tvet-embeddings"):
        """
        Initialize embedder with trained model
        
        Args:
            model_path: Path to trained TVET embedding model
        """
        if self._initialized:
            return
        
        self.model_path = Path(model_path)
        
        # Try to load custom model, fallback to default
        if self.model_path.exists():
            logger.info(f"Loading TVET model from {model_path}...")
            self.model = SentenceTransformer(str(self.model_path))
            self.is_custom = True
        else:
            logger.warning(f"Custom model not found at {model_path}")
            logger.info("Using default model: all-MiniLM-L6-v2")
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self.is_custom = False
        
        self._initialized = True
        logger.info(f"✓ Embedder ready (custom model: {self.is_custom})")
    
    def embed(
        self,
        texts: Union[str, List[str]],
        batch_size: int = 32,
        normalize: bool = True
    ) -> np.ndarray:
        """
        Generate embeddings for text(s)
        
        Args:
            texts: Single text or list of texts
            batch_size: Batch size for encoding
            normalize: Whether to normalize embeddings
            
        Returns:
            Embeddings as numpy array
        """
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            normalize_embeddings=normalize,
            show_progress_bar=False
        )
        
        return embeddings
    
    def embed_documents(
        self,
        documents: List[dict],
        text_field: str = "text"
    ) -> List[dict]:
        """
        Embed documents (with metadata preservation)
        
        Args:
            documents: List of document dicts with text_field
            text_field: Key containing text to embed
            
        Returns:
            Documents with added 'embedding' field
        """
        texts = [doc.get(text_field, "") for doc in documents]
        embeddings = self.embed(texts)
        
        for doc, embedding in zip(documents, embeddings):
            doc["embedding"] = embedding.tolist()
        
        return documents
    
    def similarity_search(
        self,
        query: str,
        documents: List[dict],
        top_k: int = 5,
        text_field: str = "text"
    ) -> List[tuple]:
        """
        Find most similar documents to query
        
        Args:
            query: Search query
            documents: List of documents (must have 'embedding' field)
            top_k: Number of results to return
            text_field: Field containing original text
            
        Returns:
            List of (document, similarity_score) tuples
        """
        query_embedding = self.embed(query)
        
        similarities = []
        for doc in documents:
            if "embedding" not in doc:
                logger.warning(f"Document missing 'embedding' field: {doc.get(text_field, '')[:50]}")
                continue
            
            doc_embedding = np.array(doc["embedding"])
            # Cosine similarity
            sim = np.dot(query_embedding[0], doc_embedding) / (
                np.linalg.norm(query_embedding[0]) * np.linalg.norm(doc_embedding) + 1e-8
            )
            similarities.append((doc, float(sim)))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def get_model_info(self) -> dict:
        """Get information about loaded model"""
        return {
            "model_name": self.model.get_sentence_embedding_dimension(),
            "embedding_dimension": self.model.get_sentence_embedding_dimension(),
            "is_custom_tvet_model": self.is_custom,
            "model_path": str(self.model_path)
        }


# Convenience functions
def embed_text(text: str) -> np.ndarray:
    """Quick embedding of single text"""
    embedder = TVETEmbedder()
    return embedder.embed(text)


def embed_texts(texts: List[str]) -> np.ndarray:
    """Quick embedding of multiple texts"""
    embedder = TVETEmbedder()
    return embedder.embed(texts)


if __name__ == "__main__":
    # Test embedding
    embedder = TVETEmbedder()
    
    test_texts = [
        "Electrical wiring safety procedures",
        "How to wire a circuit breaker",
        "Python programming basics"
    ]
    
    logger.info("Testing embeddings...")
    embeddings = embedder.embed(test_texts)
    
    logger.info(f"Embedding shape: {embeddings.shape}")
    logger.info(f"First embedding norm: {np.linalg.norm(embeddings[0]):.4f}")
    
    # Test similarity search
    documents = [
        {"text": text, "embedding": emb.tolist()}
        for text, emb in zip(test_texts, embeddings)
    ]
    
    query = "electrical safety"
    results = embedder.similarity_search(query, documents)
    
    logger.info(f"\nSimilarity search results for: '{query}'")
    for doc, score in results:
        logger.info(f"  [{score:.4f}] {doc['text']}")
