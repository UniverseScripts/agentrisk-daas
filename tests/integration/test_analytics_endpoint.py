import pytest
from fastapi import status
from db.models import PackageRiskMetric

@pytest.mark.asyncio
async def test_get_package_risk_analytics_authorized(async_client, async_session, valid_api_key):
    raw_key, api_key_model = valid_api_key
    
    metric = PackageRiskMetric(
        package_name="pypi/vllm",
        commit_velocity_24h=88,
        open_issues_delta=-2,
        fork_velocity_24h=25,
        contributor_churn=0.15,
        maintainer_count=2,
        single_maintainer_flag=False,
        days_since_last_publish=15,
        publish_cadence_variance=0.8,
        fork_spike_ratio=1.5
    )
    async_session.add(metric)
    await async_session.commit()

    response = await async_client.get(
        "/api/v1/analytics/package-risk/pypi/vllm",
        headers={"X-API-Key": raw_key}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["package_name"] == "pypi/vllm"
    assert "maintainer_concentration_index" in data
    assert "dormancy_reactivation_index" in data
    assert "anomalous_spike_index" in data
    assert data["maintainer_count"] == 2
