from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import ingest, qa, auth

app = FastAPI(title="TSS.AI Backend - FastAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
app.include_router(qa.router, prefix="/qa", tags=["qa"])
