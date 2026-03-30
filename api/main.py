from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select, update
import uvicorn

from db.connection import AsyncSessionLocal
from db.models import APIKey, RepositoryMetric
from api.schemas import RepositoryMetricResponse
from api.deps import verify_api_key
from api.rate_limiter import enforce_rate_limit

app = FastAPI(
    title="Data-as-a-Service Core",
    description="Stateless Routing Matrix - AI Developer Velocity API",
    version="1.0"
)

@app.get("/api/v1/ai-developer-velocity/{repo_name:path}", response_model=RepositoryMetricResponse)
async def get_developer_velocity(
    repo_name: str,
    auth_key: APIKey = Depends(verify_api_key)
):
    """
    Stateless GET endpoint mapping the asynchronous architecture.
    """
    # 1. Slide-window Rate Limiting Enforcement using Redis Lua
    await enforce_rate_limit(
        api_key_hash=auth_key.valid_api_keys, 
        limit=60, 
        window_secs=60
    )
    
    async with AsyncSessionLocal() as session:
        # 2. Cryptographic atomic token deduction perimeter
        # mathematically deducting without exposing race conditions 
        deduct_stmt = update(APIKey).where(
            APIKey.id == auth_key.id,
            APIKey.token_balance > 0
        ).values(
            token_balance=APIKey.token_balance - 1
        ).returning(APIKey.token_balance)
        
        deduction_result = await session.execute(deduct_stmt)
        remaining_balance = deduction_result.scalar()
        
        if remaining_balance is None:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Concurrently bankrupt token limit accessed."
            )
            
        # 3. Retrieve normalized Postgres ledger mappings
        metric_stmt = select(RepositoryMetric).where(
            RepositoryMetric.repo_name == repo_name
        ).order_by(
            RepositoryMetric.timestamp.desc()
        ).limit(1)
        
        metric_result = await session.execute(metric_stmt)
        metric_node = metric_result.scalars().first()
        
        if not metric_node:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Repository identity '{repo_name}' yields zero physical records."
            )

        # 4. Commit deterministic changes prior to socket offloading
        await session.commit()
        return metric_node

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=False)
