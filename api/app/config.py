import os
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Lexora"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api"

    DATABASE_URL: str = "postgresql://lexora:1@localhost:5432/lexora"

    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    MISTRAL_API_KEY: str = ""
    MISTRAL_MODEL: str = "ministral-8b-latest"
    MISTRAL_EMBEDDING_MODEL: str = "mistral-embed"

    FAISS_INDEX_PATH: str = "./faiss_index"
    UPLOAD_DIR: str = "./uploads"

    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "https://lexora-blond-delta.vercel.app",
    ]

    FRONTEND_URL: str = ""
    SERVE_FRONTEND: bool = False

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def strip_quotes(cls, v):
        if isinstance(v, str):
            return v.strip().strip('"').strip("'")
        return v

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v):
        import json
        if isinstance(v, str):
            v = v.strip().strip('"').strip("'")
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
                return [parsed]
            except (json.JSONDecodeError, TypeError):
                pass
            cleaned = v.strip("[]")
            return [o.strip().strip('"').strip("'") for o in cleaned.split(",") if o.strip()]
        if isinstance(v, list):
            return v
        return [str(v)]

    class Config:
        env_file = ".env"
        case_sensitive = True


def get_settings() -> Settings:
    return Settings()
