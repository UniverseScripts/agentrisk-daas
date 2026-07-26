import pytest
from scraper.github_velocity import ingest_metrics
from db.models import PackageRiskMetric
from sqlalchemy import select

@pytest.mark.asyncio
async def test_application_workflow(async_session, monkeypatch, async_client, valid_api_key):
    # This simulates a full E2E workflow:
    # 1. Scraper ingests metrics (mocking the HTTP calls)
    # 2. Database stores the metrics
    # 3. Client hits API to retrieve them
    
    raw_key, api_key_model = valid_api_key

    # Mock the fetch_*_metrics to return static payloads
    async def mock_fetch_github(*args, **kwargs):
        return {
            "rate_limited": False,
            "commit_velocity_24h": 142,
            "open_issues_delta": -5,
            "fork_velocity_24h": 38,
            "contributor_churn": 0.824
        }
        
    async def mock_fetch_npm(*args, **kwargs):
        return {
            "maintainer_count": 5,
            "days_since_last_publish": 10,
            "publish_cadence_variance": 2.5
        }
    
    monkeypatch.setattr("scraper.github_velocity.fetch_github_metrics", mock_fetch_github)
    monkeypatch.setattr("scraper.github_velocity.fetch_npm_metrics", mock_fetch_npm)
    monkeypatch.setenv("GITHUB_TOKEN", "mock_token")
    async def mock_discover(*args, **kwargs):
        return [{"name": "react", "ecosystem": "npm", "github": "facebook/react"}]
        
    monkeypatch.setattr("scraper.github_velocity.discover_target_packages", mock_discover)
    
    # 1. Run Scraper
    await ingest_metrics()
    
    # 2. Verify Database
    stmt = select(PackageRiskMetric).where(PackageRiskMetric.package_name == "npm/react")
    result = await async_session.execute(stmt)
    metric = result.scalars().first()
    assert metric is not None
    assert metric.maintainer_count == 5
    
    # 3. Client retrieves data
    response = await async_client.get(
        "/api/v1/package-risk/npm/react",
        headers={"X-API-Key": raw_key}
    )
    assert response.status_code == 200
    assert response.json()["commit_velocity_24h"] == 142
    assert response.json()["maintainer_count"] == 5
