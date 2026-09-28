"""
FORGE Application Configuration Settings
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FORGE — Forensic Object Runtime & Governed Execution"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./forge.db"
    ALLOWED_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"
    ]

settings = Settings()
