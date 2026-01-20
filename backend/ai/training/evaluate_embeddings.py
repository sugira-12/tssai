"""
Evaluate quality of trained embeddings
Measures semantic similarity and clustering quality
"""

import json
import logging
from pathlib import Path
from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingEvaluator:
    """Evaluate embedding model quality"""
    
    def __init__(self, model_path: str = "models/tvet-embeddings"):
        """
        Initialize evaluator
        
        Args:
            model_path: Path to trained model
        """
        self.model_path = Path(model_path)
        
        if self.model_path.exists():
            logger.info(f"Loading model from {model_path}...")
            self.model = SentenceTransformer(str(model_path))
        else:
            logger.warning(f"Model not found at {model_path}")
            logger.info("Using default model: all-MiniLM-L6-v2")
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
    
    def load_texts(self, texts_file: str = "datasets/training_data.json") -> List[str]:
        """Load texts for evaluation"""
        if Path(texts_file).exists():
            with open(texts_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                if isinstance(data[0], dict):
                    return [item["text"] for item in data if "text" in item]
                else:
                    return data
        
        return [
            "Electrical wiring and circuits",
            "Power distribution systems",
            "Welding techniques for metal",
            "Soldering and electronics",
            "Database design and optimization",
            "SQL query writing",
            "Plumbing pipe installation",
            "Water system maintenance"
        ]
    
    def measure_diversity(self, embeddings: np.ndarray) -> dict:
        """
        Measure embedding space diversity
        
        Args:
            embeddings: Array of embeddings
            
        Returns:
            Diversity metrics
        """
        similarity_matrix = cosine_similarity(embeddings)
        
        # Remove diagonal (self-similarity = 1.0)
        mask = ~np.eye(len(similarity_matrix), dtype=bool)
        off_diagonal = similarity_matrix[mask]
        
        return {
            "mean_similarity": float(np.mean(off_diagonal)),
            "std_similarity": float(np.std(off_diagonal)),
            "min_similarity": float(np.min(off_diagonal)),
            "max_similarity": float(np.max(off_diagonal))
        }
    
    def measure_clustering_quality(
        self,
        embeddings: np.ndarray,
        n_clusters: int = 3
    ) -> dict:
        """
        Measure how well embeddings cluster
        
        Args:
            embeddings: Array of embeddings
            n_clusters: Number of clusters
            
        Returns:
            Clustering metrics
        """
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(embeddings)
        
        # Intra-cluster similarity
        intra_cluster_sim = []
        for i in range(n_clusters):
            cluster_embeddings = embeddings[labels == i]
            if len(cluster_embeddings) > 1:
                sim = cosine_similarity(cluster_embeddings).mean()
                intra_cluster_sim.append(sim)
        
        # Inter-cluster distance
        centers = kmeans.cluster_centers_
        inter_cluster_dist = []
        for i in range(n_clusters):
            for j in range(i+1, n_clusters):
                dist = cosine_similarity(
                    [centers[i]],
                    [centers[j]]
                )[0][0]
                inter_cluster_dist.append(1 - dist)  # distance = 1 - similarity
        
        return {
            "n_clusters": n_clusters,
            "mean_intra_cluster_similarity": float(np.mean(intra_cluster_sim)),
            "mean_inter_cluster_distance": float(np.mean(inter_cluster_dist)),
            "cluster_distribution": [sum(labels == i) for i in range(n_clusters)]
        }
    
    def evaluate(self) -> dict:
        """
        Full evaluation pipeline
        
        Returns:
            Evaluation results
        """
        logger.info("=" * 70)
        logger.info("EMBEDDING EVALUATION")
        logger.info("=" * 70)
        
        # Load texts
        logger.info("\n[1] Loading texts...")
        texts = self.load_texts()
        logger.info(f"Loaded {len(texts)} texts")
        
        # Generate embeddings
        logger.info("\n[2] Generating embeddings...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        logger.info(f"Embeddings shape: {embeddings.shape}")
        
        # Diversity metrics
        logger.info("\n[3] Measuring diversity...")
        diversity = self.measure_diversity(embeddings)
        logger.info(f"Mean similarity: {diversity['mean_similarity']:.4f}")
        logger.info(f"Std deviation: {diversity['std_similarity']:.4f}")
        
        # Clustering quality
        logger.info("\n[4] Measuring clustering quality...")
        clustering = self.measure_clustering_quality(embeddings, n_clusters=3)
        logger.info(f"Intra-cluster similarity: {clustering['mean_intra_cluster_similarity']:.4f}")
        logger.info(f"Inter-cluster distance: {clustering['mean_inter_cluster_distance']:.4f}")
        
        results = {
            "model": str(self.model_path),
            "num_texts": len(texts),
            "embedding_dimension": embeddings.shape[1],
            "diversity": diversity,
            "clustering": clustering
        }
        
        # Save results
        logger.info("\n[5] Saving results...")
        output_file = Path("datasets/evaluation_results.json")
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results saved to {output_file}")
        
        logger.info("\n" + "=" * 70)
        logger.info("✅ EVALUATION COMPLETE")
        logger.info("=" * 70)
        
        return results


if __name__ == "__main__":
    evaluator = EmbeddingEvaluator()
    results = evaluator.evaluate()
