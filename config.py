try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str = "dummy_key_for_testing"
    DEFAULT_MODEL: str = "gpt-4o-mini"
    FALLBACK_MODEL: str = "gpt-3.5-turbo"
    CACHE_TTL_SECONDS: int = 300
    REDIS_URL: str = "redis://localhost:6379"
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
