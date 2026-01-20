"""
Train domain-specific embedding model for TVET content
Uses SentenceTransformers and fine-tunes on TVET documents
"""

import json
import logging
from pathlib import Path
from typing import List
import torch
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TVETEmbeddingTrainer:
    """Train and manage TVET embedding models"""
    
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        output_dir: str = "models/tvet-embeddings",
        device: str = None
    ):
        """
        Initialize trainer
        
        Args:
            model_name: HuggingFace model name
            output_dir: Directory to save trained model
            device: GPU/CPU device (auto-detected if None)
        """
        self.model_name = model_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        
        logger.info(f"Device: {self.device}")
        self.model = SentenceTransformer(model_name, device=self.device)
    
    def load_training_data(self, data_file: str = "datasets/training_data.json") -> List[str]:
        """
        Load prepared training data
        
        Args:
            data_file: Path to training data JSON
            
        Returns:
            List of text samples
        """
        logger.info(f"Loading training data from {data_file}...")
        
        if not Path(data_file).exists():
            logger.error(f"Training data file not found: {data_file}")
            logger.warning("Run prepare_data.py first to generate training data")
            return []
        
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        texts = [item["text"] for item in data if isinstance(item.get("text"), str)]
        logger.info(f"Loaded {len(texts)} text samples")
        
        return texts
    
    def generate_embeddings(self, texts: List[str], batch_size: int = 32) -> None:
        """
        Generate embeddings for all texts (no fine-tuning)
        Best for initial setup - just use pre-trained model
        
        Args:
            texts: List of text samples
            batch_size: Batch size for encoding
        """
        logger.info(f"\n[PHASE 1] Generating embeddings for {len(texts)} texts...")
        
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            batch_size=batch_size,
            convert_to_numpy=True
        )
        
        logger.info(f"Generated embeddings shape: {embeddings.shape}")
        
        # Save embeddings
        import numpy as np
        embeddings_file = self.output_dir / "embeddings.npy"
        np.save(embeddings_file, embeddings)
        logger.info(f"✓ Embeddings saved to {embeddings_file}")
        
        # Save texts reference
        texts_file = self.output_dir / "texts.json"
        with open(texts_file, "w", encoding="utf-8") as f:
            json.dump(texts, f, ensure_ascii=False, indent=2)
        logger.info(f"✓ Text references saved to {texts_file}")
    
    def fine_tune(
        self,
        texts: List[str],
        num_epochs: int = 1,
        batch_size: int = 16,
        warmup_steps: int = 100
    ) -> None:
        """
        Fine-tune embedding model on TVET data
        (Advanced - use after Phase 1)
        
        Args:
            texts: List of text samples
            num_epochs: Number of training epochs
            batch_size: Batch size for training
            warmup_steps: Warmup steps for learning rate
        """
        logger.info(f"\n[ADVANCED] Fine-tuning on {len(texts)} samples...")
        
        # Create sentence pairs (same document = similar)
        train_examples = []
        for i in range(0, len(texts)-1, 2):
            train_examples.append(InputExample(
                texts=[texts[i], texts[i+1]],
                label=0.8  # High similarity for same document
            ))
        
        train_dataloader = DataLoader(
            train_examples,
            shuffle=True,
            batch_size=batch_size
        )
        
        train_loss = losses.CosineSimilarityLoss(self.model)
        
        logger.info("Starting fine-tuning...")
        self.model.fit(
            train_objectives=[(train_dataloader, train_loss)],
            epochs=num_epochs,
            warmup_steps=warmup_steps,
            show_progress_bar=True
        )
        
        logger.info("✓ Fine-tuning complete")
    
    def save_model(self) -> None:
        """Save trained model"""
        logger.info(f"\nSaving model to {self.output_dir}...")
        self.model.save(str(self.output_dir))
        logger.info(f"✅ Model saved: {self.output_dir}")
        
        # Save metadata
        metadata = {
            "base_model": self.model_name,
            "device": self.device,
            "type": "sentence-transformer"
        }
        
        with open(self.output_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
    
    def test_embeddings(self, test_texts: List[str] = None) -> None:
        """
        Test embeddings quality
        
        Args:
            test_texts: Texts to embed and display
        """
        if test_texts is None:
            test_texts = [
                "Electrical wiring fundamentals",
                "How to install power circuits",
                "Safety protocols in construction",
                "Advanced mathematics concepts"
            ]
        
        logger.info("\n[TEST] Generating test embeddings...")
        embeddings = self.model.encode(test_texts)
        
        logger.info(f"Embedding dimension: {embeddings[0].shape}")
        logger.info(f"Sample embedding norm: {embeddings[0].norm():.4f}")
        
        # Test similarity
        from sklearn.metrics.pairwise import cosine_similarity
        similarity = cosine_similarity(embeddings)
        
        logger.info("\nSimilarity matrix:")
        logger.info(f"Text 1 vs Text 2: {similarity[0][1]:.4f}")
        logger.info(f"Text 1 vs Text 3: {similarity[0][2]:.4f}")
        logger.info(f"Text 1 vs Text 4: {similarity[0][3]:.4f}")


def main():
    """Main training pipeline"""
    logger.info("=" * 70)
    logger.info("TVET EMBEDDING MODEL TRAINING")
    logger.info("=" * 70)
    
    # Initialize trainer
    trainer = TVETEmbeddingTrainer()
    
    # Load data
    texts = trainer.load_training_data()
    
    if not texts:
        logger.warning("No training data available. Creating sample embeddings...")
        texts = [
            "Electrical systems in vehicles",
            "Welding techniques and safety",
            "Database management systems",
            "Plumbing installation methods"
        ]
    
    # Phase 1: Generate embeddings (no fine-tuning yet)
    trainer.generate_embeddings(texts)
    
    # Test embeddings
    trainer.test_embeddings()
    
    # Save model
    trainer.save_model()
    
    logger.info("\n" + "=" * 70)
    logger.info("✅ PHASE 1 COMPLETE: Domain embeddings ready for RAG")
    logger.info("=" * 70)
    logger.info(f"Model location: models/tvet-embeddings")
    logger.info("Next steps: Integrate with RAG service in embedding_service.py")


if __name__ == "__main__":
    main()
