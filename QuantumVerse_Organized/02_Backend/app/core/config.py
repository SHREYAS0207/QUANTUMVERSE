from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    APP_NAME: str = "QuantumVerse AI"
    APP_VERSION: str = "2.0.0"
    APP_URL: str = "https://quantumverse.ai"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite+aiosqlite:///./quantumverse.db"

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "quantumverse"

    SECRET_KEY: str = "change-me-in-production-use-256-bit-random-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    OPENROUTER_API_KEY: str = "your-openrouter-key-here"
    AI_MODEL: str = "meta-llama/llama-3.1-8b-instruct:free"

    REDIS_URL: str = "redis://localhost:6379/0"

    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASS: str = ""
    SMTP_FROM: str = "noreply@quantumverse.ai"

    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://quantumverse.vercel.app",
    ]

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
