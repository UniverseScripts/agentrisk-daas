import pytest
from db.models import PackageRiskMetric, APIKey
from datetime import datetime, timezone

def test_package_risk_metric_creation():
    metric = PackageRiskMetric(
        package_name="npm/react",
        commit_velocity_24h=150,
        open_issues_delta=-10,
        fork_velocity_24h=50,
        contributor_churn=0.85,
        maintainer_count=5,
        single_maintainer_flag=False,
        days_since_last_publish=10,
        publish_cadence_variance=2.5,
        fork_spike_ratio=1.2
    )
    assert metric.package_name == "npm/react"
    assert metric.commit_velocity_24h == 150
    assert metric.contributor_churn == 0.85
    assert metric.maintainer_count == 5
    assert metric.single_maintainer_flag is False
    assert metric.timestamp is None  # Handled by DB default

def test_api_key_creation():
    key = APIKey(
        valid_api_keys="hashed_secret",
        subscription_id="sub_123"
    )
    assert key.valid_api_keys == "hashed_secret"
