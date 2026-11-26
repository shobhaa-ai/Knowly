
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Knowly"
    APP_ENV: str = "development"
    DEBUG: bool = True

    GROQ_API_KEY: str

    DATABASE_URL: str = (
        "sqlite+aiosqlite:///./storage/knowly.db"
    )

    EMBEDDING_MODEL: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    CHROMA_PERSIST_DIRECTORY: str = "./storage/chroma"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
