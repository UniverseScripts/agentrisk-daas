import pytest
import sys
import importlib
from core.config import settings

def test_settings_dynamic_monkeypatch(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test_dynamic_token_123")
    assert settings.GITHUB_TOKEN == "test_dynamic_token_123"

def test_missing_resend_api_key_raises_runtime_error(monkeypatch):
    monkeypatch.setenv("RESEND_API_KEY", "")
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://mock")
    monkeypatch.setenv("REDIS_URL", "redis://mock")
    
    # Clear api.main from sys.modules to force a fresh module execution
    sys.modules.pop("api.main", None)
    
    # Assert that importing api.main directly executes its startup guard and raises RuntimeError
    with pytest.raises(RuntimeError, match="CRITICAL: RESEND_API_KEY environment variable missing"):
        importlib.import_module("api.main")
