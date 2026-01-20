# TVET Model Training - Phase 1 Setup Guide

## 🎯 What You Have Now

You now have a complete **Phase 1 training pipeline** for TVET domain-specific embeddings:

```
backend/ai/
├── training/
│   ├── prepare_data.py          → Extract PDF → Chunk text
│   ├── train_embeddings.py      → Generate embeddings
│   ├── evaluate_embeddings.py   → Measure quality
│   └── requirements.txt
├── inference/
│   └── embed_text.py            → Use embeddings in RAG
├── models/
│   └── tvet-embeddings/         → Trained model (generated)
└── datasets/
    ├── tvet_books/              → Place your PDFs here
    ├── training_data.json       → Generated
    └── evaluation_results.json  → Generated
```

---

## 📋 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
cd backend
pip install -r ai/training/requirements.txt
```

**What gets installed:**
- `sentence-transformers` - Embedding model
- `torch` - PyTorch (ML framework)
- `faiss-cpu` - Vector search
- `pypdf` - PDF reading
- `scikit-learn` - Evaluation metrics

### Step 2: Add Your PDF Files

Place TVET books/modules in:
```
backend/ai/datasets/tvet_books/
```

Examples:
- `welding_fundamentals.pdf`
- `electrical_systems_module.pdf`
- `database_design_guide.pdf`

### Step 3: Run Training Pipeline

```bash
cd backend

# Step A: Prepare data (Extract PDFs → Chunks)
python ai/training/prepare_data.py

# Step B: Train embeddings
python ai/training/train_embeddings.py

# Step C: Evaluate quality (optional)
python ai/training/evaluate_embeddings.py
```

---

## 🔍 What Each Script Does

### 1. `prepare_data.py` 
**Purpose:** Extract text from PDFs and create training dataset

**Input:**
- PDFs in `datasets/tvet_books/`

**Output:**
- `datasets/training_data.json` - 512-char chunks with metadata

**Run:**
```bash
python ai/training/prepare_data.py
```

### 2. `train_embeddings.py`
**Purpose:** Generate TVET-specific embeddings using SentenceTransformers

**What happens:**
1. Loads pre-trained `all-MiniLM-L6-v2` model
2. Encodes all TVET texts
3. Saves model to `models/tvet-embeddings/`

**Output:**
- `models/tvet-embeddings/` - Ready-to-use model
- `models/tvet-embeddings/embeddings.npy` - Vectors
- `models/tvet-embeddings/texts.json` - Text references

**Run:**
```bash
python ai/training/train_embeddings.py
```

**Time:** ~1-5 minutes (CPU), ~30 seconds (GPU)

### 3. `evaluate_embeddings.py`
**Purpose:** Measure embedding quality

**Metrics calculated:**
- Embedding diversity (how spread out vectors are)
- Clustering quality (semantic grouping)
- Similarity patterns

**Output:**
- `datasets/evaluation_results.json`

**Run:**
```bash
python ai/training/evaluate_embeddings.py
```

---

## 🔗 Integration with RAG

Your trained model automatically integrates with the RAG system:

### Current Code (in `services/embedding_service.py`)

Replace this:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
```

With this:
```python
from backend.ai.inference.embed_text import TVETEmbedder
embedder = TVETEmbedder()  # Auto-loads trained model
embeddings = embedder.embed(texts)
```

---

## 📊 Expected Results

After running the pipeline:

**1. Training Data**
```
Total documents: X
Total chunks: ~Y
Chunk size: 512 characters with 50-char overlap
```

**2. Embeddings Generated**
```
- Dimension: 384
- Format: Normalized L2 vectors
- Count: One per chunk
```

**3. Quality Metrics**
```
- Mean similarity: 0.3-0.5 (good diversity)
- Clustering: Clear semantic grouping
- Ready for RAG semantic search
```

---

## ⚙️ Customization

### Change Model Size
Edit `train_embeddings.py`:

```python
# Smaller (faster, less accurate)
SentenceTransformer("all-MiniLM-L6-v2")

# Larger (slower, more accurate) 
SentenceTransformer("all-mpnet-base-v2")
```

### Adjust Chunk Size
Edit `prepare_data.py`:

```python
chunks = chunk_text(doc["content"], 
    chunk_size=256,  # Smaller chunks
    overlap=25
)
```

### Fine-tune on Your Data (Advanced)
Edit `train_embeddings.py`:

```python
# After generate_embeddings()
trainer.fine_tune(texts, num_epochs=3)
trainer.save_model()
```

---

## 🐛 Troubleshooting

### "No module named 'sentence_transformers'"
```bash
pip install sentence-transformers torch
```

### "No PDF files found"
- Check `backend/ai/datasets/tvet_books/` exists
- Add .pdf files to that folder

### Out of memory error
- Use smaller batch_size in scripts
- Or use `faiss-cpu` instead of GPU

### Very slow embedding generation
- Use GPU: Install `torch` with CUDA
- Or use smaller pre-trained model

---

## 🚀 Next Phase (After Phase 1 Works)

Once embeddings are trained:

**Option 1: Fine-tune with Q&A pairs** (5min setup)
- Create TVET question-answer pairs
- Fine-tune embeddings to understand context

**Option 2: Add metadata ranking** (10min setup)
- Tag chunks by trade/module/difficulty
- Improve ranking in RAG results

**Option 3: Local LLM inference** (30min setup)
- Add Mistral or LLaMA for answer generation
- Complete offline RAG system

**Option 4: Evaluation & metrics** (20min setup)
- Measure RAG accuracy on test questions
- Optimize chunking strategy

---

## 📝 File Structure After Running

```
backend/ai/
├── datasets/
│   ├── tvet_books/              ← Your PDFs
│   ├── training_data.json       ✅ (generated)
│   └── evaluation_results.json  ✅ (generated)
├── models/
│   └── tvet-embeddings/
│       ├── pytorch_model.bin    ✅ (trained model)
│       ├── embeddings.npy       ✅ (vectors)
│       ├── texts.json           ✅ (references)
│       └── metadata.json        ✅ (model info)
├── training/
│   ├── prepare_data.py
│   ├── train_embeddings.py
│   ├── evaluate_embeddings.py
│   └── requirements.txt
└── inference/
    └── embed_text.py
```

---

## ✅ Checklist

- [ ] Install dependencies: `pip install -r ai/training/requirements.txt`
- [ ] Add PDFs to `datasets/tvet_books/`
- [ ] Run: `python ai/training/prepare_data.py`
- [ ] Run: `python ai/training/train_embeddings.py`
- [ ] Check output in `models/tvet-embeddings/`
- [ ] (Optional) Run: `python ai/training/evaluate_embeddings.py`
- [ ] Update `embedding_service.py` to use `TVETEmbedder`
- [ ] Test RAG with new embeddings

---

**You're ready to train! Start with Step 1 above.** 🚀
