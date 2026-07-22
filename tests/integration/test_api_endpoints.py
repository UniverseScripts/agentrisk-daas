import pytest
from fastapi import status
from db.models import RepositoryMetric

@pytest.mark.asyncio
async def test_get_developer_velocity_unauthorized(async_client):
    response = await async_client.get("/api/v1/ai-developer-velocity/pytorch/pytorch")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.asyncio
async def test_get_developer_velocity_authorized(async_client, async_session, valid_api_key):
    raw_key, api_key_model = valid_api_key
    
    # Seed metric with technographic signals
    metric = RepositoryMetric(
        repo_name="pytorch/pytorch",
        commit_velocity_24h=142,
        open_issues_delta=-5,
        fork_velocity_24h=38,
        contributor_churn=0.824,
        framework_shifts='["pytorch -> triton"]',
        license_type="Apache-2.0",
        license_drift=False,
        model_weight_formats='["GGUF", "Safetensors"]'
    )
    async_session.add(metric)
    await async_session.commit()

    response = await async_client.get(
        "/api/v1/ai-developer-velocity/pytorch/pytorch",
        headers={"X-API-Key": raw_key}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["repo_name"] == "pytorch/pytorch"
    assert data["commit_velocity_24h"] == 142
    assert data["license_type"] == "Apache-2.0"
    assert data["license_drift"] is False

@pytest.mark.asyncio
async def test_lemon_squeezy_webhook(async_client):
    import hmac
    import hashlib
    import json
    
    secret = "mock_secret"
    payload = {
        "meta": {"event_name": "order_created"},
        "data": {"attributes": {"user_email": "b2b_subscriber@enterprise.com"}}
    }
    raw_body = json.dumps(payload).encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    
    response = await async_client.post(
        "/webhooks/lemon-squeezy",
        content=raw_body,
        headers={"X-Signature": signature, "Content-Type": "application/json"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "success"

