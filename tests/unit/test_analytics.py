import pytest
from db.models import RepositoryMetric
from api.analytics import calculate_fmdi, calculate_cffi, calculate_prei, calculate_llrs

def test_analytics_fmdi_calculation():
    metric = RepositoryMetric(
        repo_name="pytorch/pytorch",
        commit_velocity_24h=100,
        contributor_churn=0.2,
        framework_shifts='["pytorch -> triton"]'
    )
    fmdi = calculate_fmdi(metric)
    assert isinstance(fmdi, float)
    assert fmdi > 0

def test_analytics_cffi_calculation():
    metric = RepositoryMetric(
        repo_name="pytorch/pytorch",
        commit_velocity_24h=50,
        open_issues_delta=15,
        contributor_churn=0.8
    )
    cffi = calculate_cffi(metric)
    assert isinstance(cffi, float)
    assert 0.0 <= cffi <= 10.0

def test_analytics_prei_calculation():
    metric = RepositoryMetric(
        repo_name="pytorch/pytorch",
        model_weight_formats='["GGUF", "AWQ", "Safetensors"]',
        fine_tuning_frameworks='["Unsloth", "PEFT"]'
    )
    prei = calculate_prei(metric)
    assert isinstance(prei, float)
    assert prei >= 7.0

def test_analytics_llrs_calculation():
    metric_safe = RepositoryMetric(license_type="Apache-2.0", license_drift=False)
    assert calculate_llrs(metric_safe) == 1.5

    metric_risky = RepositoryMetric(license_type="AGPL-3.0", license_drift=True)
    assert calculate_llrs(metric_risky) == 10.0
