import pytest
from scraper.github_velocity import ingest_metrics
from db.models import RepositoryMetric
from sqlalchemy import select

@pytest.mark.asyncio
async def test_application_workflow(async_session, monkeypatch, async_client, valid_api_key):
    # This simulates a full E2E workflow:
    # 1. Scraper ingests metrics (mocking the HTTP calls)
    # 2. Database stores the metrics
    # 3. Client hits API to retrieve them
    
    raw_key, api_key_model = valid_api_key

    # Mock the fetch_repository_metrics to return a static payload
    async def mock_fetch(*args, **kwargs):
        return {
            "rate_limited": False,
            "repo_name": "pytorch/pytorch",
            "commit_velocity_24h": 142,
            "open_issues_delta": -5,
            "fork_velocity_24h": 38,
            "contributor_churn": 0.824
        }
    
    monkeypatch.setattr("scraper.github_velocity.fetch_repository_metrics", mock_fetch)
    monkeypatch.setenv("GITHUB_TOKEN", "mock_token")
    monkeypatch.setattr("scraper.github_velocity.TARGET_REPOSITORIES", ["pytorch/pytorch"])
    
    # 1. Run Scraper
    await ingest_metrics()
    
    # 2. Verify Database
    stmt = select(RepositoryMetric).where(RepositoryMetric.repo_name == "pytorch/pytorch")
    result = await async_session.execute(stmt)
    metric = result.scalars().first()
    assert metric is not None
    
    # 3. Client retrieves data
    response = await async_client.get(
        "/api/v1/ai-developer-velocity/pytorch/pytorch",
        headers={"X-API-Key": raw_key}
    )
    assert response.status_code == 200
    assert response.json()["commit_velocity_24h"] == 142
