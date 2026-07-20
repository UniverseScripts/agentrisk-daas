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
    
    # Seed metric
    metric = RepositoryMetric(
        repo_name="pytorch/pytorch",
        commit_velocity_24h=142,
        open_issues_delta=-5,
        fork_velocity_24h=38,
        contributor_churn=0.824
    )
    async_session.add(metric)
    await async_session.commit()

    # Wait, the app uses a mocked Redis instance for rate_limiter?
    # We should patch the rate limiter or use fakeredis.
    # For now, let's patch enforce_rate_limit to pass always in tests.
    
    response = await async_client.get(
        "/api/v1/ai-developer-velocity/pytorch/pytorch",
        headers={"X-API-Key": raw_key}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["repo_name"] == "pytorch/pytorch"
    assert data["commit_velocity_24h"] == 142
