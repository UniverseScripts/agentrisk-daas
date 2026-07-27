import os
import sys
from pydantic_settings import BaseSettings, SettingsConfigDict

# Ensure project root is in sys.path when imported across modules/scripts
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

class Settings(BaseSettings):
    """
    Centralized, typed Pydantic Settings configuration manager.
    Parses environment variables dynamically from environment or .env file.
    Default empty string fallbacks allow isolated script runs while application
    startup logic enforces strict fail-fast validation.
    """
    DATABASE_URL: str = ""
    REDIS_URL: str = ""
    GITHUB_TOKEN: str = ""
    RESEND_API_KEY: str = ""
    LEMON_SQUEEZY_WEBHOOK_SECRET: str = ""
    LEMON_SQUEEZY_VARIANT_ID: str = ""

    model_config = SettingsConfigDict(
        env_file=os.path.join(project_root, ".env") if os.path.exists(os.path.join(project_root, ".env")) else None,
        env_file_encoding="utf-8",
        extra="ignore"
    )

def get_settings() -> Settings:
    """Returns a fresh Settings instance dynamically reflecting live environment."""
    return Settings()

class SettingsProxy:
    """Dynamic proxy delegating attribute access to fresh get_settings() calls to support monkeypatching."""
    def __getattr__(self, name: str):
        return getattr(get_settings(), name)

settings = SettingsProxy()
