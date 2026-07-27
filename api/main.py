from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy import select, update
import uvicorn
import os
import hmac
import hashlib
import uuid
import httpx
from db.connection import AsyncSessionLocal
from db.models import APIKey, PackageRiskMetric
from api.schemas import PackageRiskMetricResponse, AdvancedPackageRiskAnalyticsResponse
from api.deps import verify_api_key
from api.rate_limiter import enforce_rate_limit
from api.analytics import calculate_mci, calculate_dri, calculate_asi

from core.config import settings

# Enforce strict fail-fast perimeter checks on application boot
if not settings.RESEND_API_KEY:
    raise RuntimeError("CRITICAL: RESEND_API_KEY environment variable missing")
if not settings.DATABASE_URL:
    raise RuntimeError("CRITICAL: DATABASE_URL environment variable missing")
if not settings.REDIS_URL:
    raise RuntimeError("CRITICAL: REDIS_URL environment variable missing")

app = FastAPI(
    title="Data-as-a-Service Core",
    description="Maintainer & Dormancy Risk Signal DaaS",
    version="2.0"
)

@app.post("/webhooks/lemon-squeezy")
@app.post("/api/v1/webhooks/lemon-squeezy")
async def lemon_squeezy_webhook(request: Request):
    """
    Cryptographic Webhook Receiver for Lemon Squeezy MoR.
    Strictly verifies HMAC signatures to allocate API tokens securely.
    """
    if not settings.LEMON_SQUEEZY_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="CRITICAL: LEMON_SQUEEZY_WEBHOOK_SECRET environment variable missing"
        )
        
    x_signature = request.headers.get("X-Signature")
    if not x_signature:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing signature headers")
        
    raw_body = await request.body()
    
    digest = hmac.new(
        settings.LEMON_SQUEEZY_WEBHOOK_SECRET.encode("utf-8"), 
        raw_body, 
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(digest, x_signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Signature authentication forgery detected")
        
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unparsable JSON transmission")
        
    meta = payload.get("meta", {})
    event_name = meta.get("event_name")
    
    valid_events = ["subscription_created", "subscription_payment_success", "subscription_updated", "subscription_cancelled", "subscription_expired"]
    if event_name not in valid_events:
        return {"status": "Event ignored properly"}
        
    data = payload.get("data", {})
    attributes = data.get("attributes", {})
    user_email = attributes.get("user_email")
    variant_id = attributes.get("variant_id")
    subscription_id = data.get("id")
    
    if not user_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing user_email payload structure")

    key_dispatched = False

    if event_name == "subscription_created":
        # TODO: Fail closed in production when LEMON_SQUEEZY_VARIANT_ID is definitively set.
        if settings.LEMON_SQUEEZY_VARIANT_ID and str(variant_id) != str(settings.LEMON_SQUEEZY_VARIANT_ID):
            return {"status": "Ignored - different product variant"}

        raw_api_key = f"daas_live_{uuid.uuid4().hex}"
        hashed_api_key = hashlib.sha256(raw_api_key.encode("utf-8")).hexdigest()
        
        async with AsyncSessionLocal() as session:
            new_api_key = APIKey(
                valid_api_keys=hashed_api_key,
                subscription_id=str(subscription_id),
                is_active=True
            )
            session.add(new_api_key)
            await session.commit()
            
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    "https://api.resend.com/emails",
                    headers={
                        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "from": "onboarding@yourdomain.com",
                        "to": [user_email],
                        "subject": "Your Maintainer Risk DaaS API Key",
                        "html": f"<p>Thank you for subscribing. Your API key is: <strong>{raw_api_key}</strong></p>"
                    },
                    timeout=10.0
                )
                res.raise_for_status()
                key_dispatched = True
        except Exception as e:
            # We strictly log this and fail the dispatch flag, alerting the MoR or dashboard
            print(f"CRITICAL ALERT: Failed to dispatch API key email to {user_email}. Error: {e}")
            key_dispatched = False
            
    elif event_name in ["subscription_cancelled", "subscription_expired"]:
        async with AsyncSessionLocal() as session:
            stmt = update(APIKey).where(APIKey.subscription_id == str(subscription_id)).values(is_active=False)
            await session.execute(stmt)
            await session.commit()
            print(f"Subscription {subscription_id} cancelled/expired. Key deactivated.")

    return {
        "status": "success", 
        "provisioned": event_name == "subscription_created",
        "key_dispatched": key_dispatched
    }

@app.get("/", description="Check the application's health")
async def GetHealth():
    return {"status": "online"}

@app.get("/api/v1/package-risk/{package_name:path}", response_model=PackageRiskMetricResponse)
async def get_package_risk(
    package_name: str,
    auth_key: APIKey = Depends(verify_api_key)
):
    """
    Returns latest raw package_risk_metrics row.
    """
    await enforce_rate_limit(
        api_key_hash=auth_key.valid_api_keys, 
        limit=60, 
        window_secs=60
    )
    
    async with AsyncSessionLocal() as session:
        metric_stmt = select(PackageRiskMetric).where(
            PackageRiskMetric.package_name == package_name
        ).order_by(
            PackageRiskMetric.timestamp.desc()
        ).limit(1)
        
        metric_result = await session.execute(metric_stmt)
        metric_node = metric_result.scalars().first()
        
        if not metric_node:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Package identity '{package_name}' yields zero physical records."
            )

        return metric_node

@app.get("/api/v1/analytics/package-risk/{package_name:path}", response_model=AdvancedPackageRiskAnalyticsResponse)
async def get_package_risk_analytics(
    package_name: str,
    auth_key: APIKey = Depends(verify_api_key)
):
    """
    Synthesizes raw metrics into institutional composite indices (MCI, DRI, ASI).
    """
    await enforce_rate_limit(
        api_key_hash=auth_key.valid_api_keys, 
        limit=60, 
        window_secs=60
    )
    
    async with AsyncSessionLocal() as session:
        metric_stmt = select(PackageRiskMetric).where(
            PackageRiskMetric.package_name == package_name
        ).order_by(
            PackageRiskMetric.timestamp.desc()
        ).limit(1)
        
        metric_result = await session.execute(metric_stmt)
        metric_node = metric_result.scalars().first()
        
        if not metric_node:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Package identity '{package_name}' yields zero physical records."
            )

        return {
            "package_name": metric_node.package_name,
            "timestamp": metric_node.timestamp,
            "maintainer_concentration_index": calculate_mci(metric_node),
            "dormancy_reactivation_index": calculate_dri(metric_node),
            "anomalous_spike_index": calculate_asi(metric_node),
            "maintainer_count": metric_node.maintainer_count,
            "single_maintainer_flag": metric_node.single_maintainer_flag,
            "days_since_last_publish": metric_node.days_since_last_publish,
            "publish_cadence_variance": metric_node.publish_cadence_variance,
            "fork_spike_ratio": metric_node.fork_spike_ratio,
        }

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, env_file=".env", reload=True)
