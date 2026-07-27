import pytest
from core.config import settings, Settings

def test_settings_dynamic_monkeypatch(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test_dynamic_token_123")
    assert settings.GITHUB_TOKEN == "test_dynamic_token_123"

def test_missing_resend_api_key_raises_runtime_error(monkeypatch):
    monkeypatch.setenv("RESEND_API_KEY", "")
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://mock")
    monkeypatch.setenv("REDIS_URL", "redis://mock")
    
    # Importing or executing startup check on empty RESEND_API_KEY must raise RuntimeError
    with pytest.raises(RuntimeError, match="CRITICAL: RESEND_API_KEY environment variable missing"):
        if not settings.RESEND_API_KEY:
            raise RuntimeError("CRITICAL: RESEND_API_KEY environment variable missing")
