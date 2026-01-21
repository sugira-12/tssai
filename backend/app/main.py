# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.api import ingest, qa, quiz

# Create FastAPI app
app = FastAPI(
    title="TSS.AI Backend - FastAPI",
    description="Backend API for TVET document ingestion, Q&A, and quiz generation.",
    version="0.1.0",
)

# Enable CORS for frontend connections (localhost / dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with prefixes and tags
app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
app.include_router(qa.router, prefix="/qa", tags=["qa"])
app.include_router(quiz.router, prefix="/quiz", tags=["quiz"])

# Root endpoint
@app.get("/", summary="Root endpoint")
async def root():
    return {"message": "Welcome to TSS.AI Backend! Visit /docs for API documentation."}
