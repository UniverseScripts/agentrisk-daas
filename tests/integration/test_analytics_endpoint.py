import pytest
from fastapi import status
from db.models import RepositoryMetric

@pytest.mark.asyncio
async def test_get_developer_velocity_analytics_authorized(async_client, async_session, valid_api_key):
    raw_key, api_key_model = valid_api_key
    
    metric = RepositoryMetric(
        repo_name="vllm-project/vllm",
        commit_velocity_24h=88,
        open_issues_delta=-2,
        fork_velocity_24h=25,
        contributor_churn=0.15,
        framework_shifts='["vllm_integration"]',
        license_type="Apache-2.0",
        license_drift=False,
        model_weight_formats='["AWQ", "Safetensors"]',
        fine_tuning_frameworks='["PEFT"]'
    )
    async_session.add(metric)
    await async_session.commit()

    response = await async_client.get(
        "/api/v1/analytics/ai-developer-velocity/vllm-project/vllm",
        headers={"X-API-Key": raw_key}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["repo_name"] == "vllm-project/vllm"
    assert "framework_migration_index" in data
    assert "contributor_flight_risk" in data
    assert "production_readiness_score" in data
    assert "license_liability_score" in data
    assert data["license_type"] == "Apache-2.0"
