import os
os.environ["DATABASE_URL"] = "postgresql+asyncpg://mock"
os.environ["REDIS_URL"] = "redis://mock"
os.environ["LEMON_SQUEEZY_WEBHOOK_SECRET"] = "mock_secret"

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from fastapi.testclient import TestClient
import httpx

from db.models import Base
from api.main import app
from db.models import APIKey

# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

@pytest_asyncio.fixture(scope="function")
async def async_session():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        yield session
        
    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(autouse=True)
def patch_environment(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://mock")
    monkeypatch.setenv("REDIS_URL", "redis://mock")
    monkeypatch.setenv("LEMON_SQUEEZY_WEBHOOK_SECRET", "mock_secret")

@pytest.fixture(autouse=True)
def patch_db_session(monkeypatch, async_session):
    # Patch the global AsyncSessionLocal to use our test session factory
    monkeypatch.setattr("api.main.AsyncSessionLocal", TestingSessionLocal)
    monkeypatch.setattr("api.deps.AsyncSessionLocal", TestingSessionLocal)
    monkeypatch.setattr("scraper.github_velocity.AsyncSessionLocal", TestingSessionLocal)
    
    # Patch rate limiter to allow tests to run without Redis
    async def mock_rate_limit(*args, **kwargs):
        pass
    monkeypatch.setattr("api.main.enforce_rate_limit", mock_rate_limit)

@pytest_asyncio.fixture(scope="function")
async def async_client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture(scope="function")
async def valid_api_key(async_session):
    import hashlib
    raw_key = "test_api_key"
    hashed_key = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()
    api_key = APIKey(valid_api_keys=hashed_key, token_balance=100)
    async_session.add(api_key)
    await async_session.commit()
    return raw_key, api_key
