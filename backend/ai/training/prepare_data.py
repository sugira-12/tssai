"""
Prepare TVET training data from PDF books and documents
Extracts text from PDFs and chunks them for embedding training
"""

import os
import logging
from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_pdfs(folder_path: str) -> List[Dict[str, str]]:
    """
    Load all PDFs from a folder and extract text
    
    Args:
        folder_path: Path to folder containing PDF files
        
    Returns:
        List of dictionaries with file info and text content
    """
    docs = []
    folder = Path(folder_path)
    
    if not folder.exists():
        logger.warning(f"Dataset folder not found: {folder_path}")
        return docs
    
    pdf_files = list(folder.glob("*.pdf"))
    logger.info(f"Found {len(pdf_files)} PDF files")
    
    for pdf_file in pdf_files:
        try:
            logger.info(f"Processing: {pdf_file.name}")
            reader = PdfReader(pdf_file)
            
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and text.strip():
                    docs.append({
                        "source": pdf_file.name,
                        "page": page_num + 1,
                        "content": text,
                        "metadata": {
                            "file": pdf_file.name,
                            "page": page_num + 1,
                            "total_pages": len(reader.pages)
                        }
                    })
            
            logger.info(f"✓ Extracted {len(reader.pages)} pages from {pdf_file.name}")
        
        except Exception as e:
            logger.error(f"Error processing {pdf_file.name}: {str(e)}")
            continue
    
    return docs


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks
    
    Args:
        text: Text to chunk
        chunk_size: Size of each chunk in characters
        overlap: Overlap between chunks
        
    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        
        if chunk.strip():
            chunks.append(chunk)
        
        start = end - overlap
    
    return chunks


def prepare_training_data(
    input_folder: str = "datasets/tvet_books",
    output_file: str = "datasets/training_data.json"
) -> None:
    """
    Full pipeline: Load PDFs → Chunk text → Save JSON
    
    Args:
        input_folder: Folder containing PDF files
        output_file: Output JSON file path
    """
    logger.info("=" * 60)
    logger.info("TVET DATA PREPARATION PIPELINE")
    logger.info("=" * 60)
    
    # Step 1: Load PDFs
    logger.info("\n[STEP 1] Loading PDFs...")
    docs = load_pdfs(input_folder)
    
    if not docs:
        logger.warning("No documents loaded. Add PDF files to datasets/tvet_books/")
        return
    
    logger.info(f"Total documents loaded: {len(docs)}")
    
    # Step 2: Chunk documents
    logger.info("\n[STEP 2] Chunking documents...")
    training_data = []
    
    for doc in docs:
        chunks = chunk_text(doc["content"])
        for chunk_idx, chunk in enumerate(chunks):
            training_data.append({
                "text": chunk,
                "source": doc["source"],
                "page": doc["page"],
                "chunk": chunk_idx,
                "metadata": doc["metadata"]
            })
    
    logger.info(f"Total chunks created: {len(training_data)}")
    
    # Step 3: Save training data
    logger.info("\n[STEP 3] Saving training data...")
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(training_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"✅ Training data saved to: {output_path}")
    logger.info(f"Total samples: {len(training_data)}")
    logger.info("=" * 60)


if __name__ == "__main__":
    prepare_training_data()
