import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# Air-gapped configurations loaded dynamically
# Default to an empty string to prevent import crash, but validate immediately when connecting.
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("Critical Security Violation: DATABASE_URL environment variable is missing.")

# Utilize asyncpg driver. Echo is explicitly disabled for production parity and resource conservation.
# Serverless pooling tuned specifically for Neon Serverless PostgreSQL.
engine = create_async_engine(
    DATABASE_URL, 
    echo=False,
    pool_recycle=300,      # Recycle connections to handle idle serverless drops
    pool_pre_ping=True,    # Verify connection sanity prior to checkout
    pool_size=5,           # Optimized connection pool size for serverless limits
    max_overflow=10,       # Allows burst connections during peak requests
    pool_timeout=30        # Drop request gracefully after 30s timeout
)

# Async session factory to manage the lifecycle of database operations
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)
