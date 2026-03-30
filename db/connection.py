import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# Air-gapped configurations loaded dynamically
# Default to an empty string to prevent import crash, but validate immediately when connecting.
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("Critical Security Violation: DATABASE_URL environment variable is missing.")

# Utilize asyncpg driver. Echo is explicitly disabled for production parity and resource conservation.
engine = create_async_engine(
    DATABASE_URL, 
    echo=False,
    pool_size=20,          # Maintains a steady baseline of 20 connections
    max_overflow=10,       # Allows 10 burst connections during spikes
    pool_timeout=30        # Drops request gracefully after 30s rather than hanging Uvicorn
)

# Async session factory to manage the lifecycle of database operations
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)
