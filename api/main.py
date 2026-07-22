from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy import select, update
import uvicorn
import os
import hmac
import hashlib
import uuid
from db.connection import AsyncSessionLocal
from db.models import APIKey, RepositoryMetric
from api.schemas import RepositoryMetricResponse, AdvancedTechnographicAnalyticsResponse
from api.deps import verify_api_key
from api.rate_limiter import enforce_rate_limit
from api.analytics import calculate_fmdi, calculate_cffi, calculate_prei, calculate_llrs

app = FastAPI(
    title="Data-as-a-Service Core",
    description="Stateless Routing Matrix - AI Developer Velocity API",
    version="1.0"
)

LEMON_SQUEEZY_WEBHOOK_SECRET = os.getenv("LEMON_SQUEEZY_WEBHOOK_SECRET")

@app.post("/webhooks/lemon-squeezy")
@app.post("/api/v1/webhooks/lemon-squeezy")
async def lemon_squeezy_webhook(request: Request):
    """
    Cryptographic Webhook Receiver for Lemon Squeezy MoR.
    Strictly verifies HMAC signatures to allocate 10000 limit API tokens securely.
    """
    if not LEMON_SQUEEZY_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="CRITICAL: LEMON_SQUEEZY_WEBHOOK_SECRET environment variable missing"
        )
        
    x_signature = request.headers.get("X-Signature")
    if not x_signature:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing signature headers")
        
    # Read raw body strictly for HMAC calculation without parsing JSON
    raw_body = await request.body()
    
    # Compute HMAC SHA-256 Digest mathematically
    digest = hmac.new(
        LEMON_SQUEEZY_WEBHOOK_SECRET.encode("utf-8"), 
        raw_body, 
        hashlib.sha256
    ).hexdigest()
    
    # Secure constant-time comparison to prevent timing attacks
    if not hmac.compare_digest(digest, x_signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Signature authentication forgery detected")
        
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unparsable JSON transmission")
        
    # Isolate relevant payload keys
    meta = payload.get("meta", {})
    if meta.get("event_name") != "order_created":
        return {"status": "Event ignored properly"}
        
    data = payload.get("data", {})
    attributes = data.get("attributes", {})
    user_email = attributes.get("user_email")
    
    if not user_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing user_email payload structure")
    
    # Cryptographic API String generation
    raw_api_key = f"daas_live_{uuid.uuid4().hex}"
    
    # Non-reversible SHA-256 standard encryption for the ledger
    hashed_api_key = hashlib.sha256(raw_api_key.encode("utf-8")).hexdigest()
    
    # Atomic Asynchronous Ledger Injection
    async with AsyncSessionLocal() as session:
        new_api_key = APIKey(
            valid_api_keys=hashed_api_key,
            token_balance=10000,
            is_active=True
        )
        session.add(new_api_key)
        await session.commit()
        
    # Output stub exactly as required
    print(f"Provisioned key for {user_email}. Raw Key: {raw_api_key}")
    # TODO: Async dispatch raw_api_key to client_email
    
    return {"status": "success", "provisioned": True}

@app.get("/", description="Check the application's health")
async def GetHealth():
    return {"status": "online"}

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

@app.get("/api/v1/analytics/ai-developer-velocity/{repo_name:path}", response_model=AdvancedTechnographicAnalyticsResponse)
async def get_developer_velocity_analytics(
    repo_name: str,
    auth_key: APIKey = Depends(verify_api_key)
):
    """
    Synthesizes raw AST technographic metrics into institutional composite indices (FMDI, CFFI, PREI, LLRS).
    """
    await enforce_rate_limit(
        api_key_hash=auth_key.valid_api_keys, 
        limit=60, 
        window_secs=60
    )
    
    async with AsyncSessionLocal() as session:
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

        await session.commit()

        # Compute composite indices
        return {
            "repo_name": metric_node.repo_name,
            "timestamp": metric_node.timestamp,
            "framework_migration_index": calculate_fmdi(metric_node),
            "contributor_flight_risk": calculate_cffi(metric_node),
            "production_readiness_score": calculate_prei(metric_node),
            "license_liability_score": calculate_llrs(metric_node),
            "license_type": metric_node.license_type,
            "license_drift": metric_node.license_drift,
            "framework_shifts": metric_node.framework_shifts,
            "model_weight_formats": metric_node.model_weight_formats,
            "fine_tuning_frameworks": metric_node.fine_tuning_frameworks,
        }

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, env_file=".env", reload=True)
