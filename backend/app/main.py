from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import ingest, qa, quiz

app = FastAPI(title="TSS.AI Backend - FastAPI")

# Enable CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
app.include_router(qa.router, prefix="/qa", tags=["qa"])
app.include_router(quiz.router, prefix="/quiz", tags=["quiz"])
