import pytest
from db.models import RepositoryMetric, APIKey
from datetime import datetime, timezone

def test_repository_metric_creation():
    metric = RepositoryMetric(
        repo_name="pytorch/pytorch",
        commit_velocity_24h=150,
        open_issues_delta=-10,
        fork_velocity_24h=50,
        contributor_churn=0.85,
        framework_shifts='["pytorch -> triton"]',
        license_type="Apache-2.0",
        license_drift=False,
        model_weight_formats='["GGUF", "Safetensors"]'
    )
    assert metric.repo_name == "pytorch/pytorch"
    assert metric.commit_velocity_24h == 150
    assert metric.contributor_churn == 0.85
    assert metric.license_type == "Apache-2.0"
    assert metric.license_drift is False
    assert metric.timestamp is None  # Handled by DB default

def test_api_key_creation():
    key = APIKey(
        valid_api_keys="hashed_secret",
        token_balance=5000
    )
    assert key.valid_api_keys == "hashed_secret"
    assert key.token_balance == 5000
