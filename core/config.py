import os
import sys
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

# Ensure project root is in sys.path when imported across modules/scripts
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

class Settings(BaseSettings):
    """
    Centralized, typed Pydantic Settings configuration manager.
    Parses and strictly validates environment variables from host environment or .env file.
    """
    DATABASE_URL: str
    REDIS_URL: str
    GITHUB_TOKEN: str
    RESEND_API_KEY: str
    LEMON_SQUEEZY_WEBHOOK_SECRET: str
    LEMON_SQUEEZY_VARIANT_ID: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(project_root, ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
