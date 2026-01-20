import os

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tssai.db")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "data/uploads")

settings = Settings()
