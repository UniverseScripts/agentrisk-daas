import pytest
from db.models import PackageRiskMetric
from api.analytics import calculate_mci, calculate_dri, calculate_asi

def test_analytics_mci_calculation():
    metric = PackageRiskMetric(
        package_name="npm/react",
        maintainer_count=1,
        contributor_churn=0.8
    )
    mci = calculate_mci(metric)
    assert isinstance(mci, float)
    assert mci == 10.0

def test_analytics_mci_insufficient_data():
    metric = PackageRiskMetric(
        package_name="npm/react",
        maintainer_count=None,
        contributor_churn=0.8
    )
    mci = calculate_mci(metric)
    assert mci == "insufficient data"

def test_analytics_dri_calculation():
    metric = PackageRiskMetric(
        package_name="npm/react",
        days_since_last_publish=630,
        publish_cadence_variance=1.5
    )
    dri = calculate_dri(metric)
    assert isinstance(dri, float)
    assert dri == 10.0

def test_analytics_dri_insufficient_data():
    metric = PackageRiskMetric(
        package_name="npm/react",
        days_since_last_publish=None,
        publish_cadence_variance=1.5
    )
    dri = calculate_dri(metric)
    assert dri == "insufficient data"

def test_dri_insufficient_data_on_single_publish():
    metric = PackageRiskMetric(
        package_name="npm/react",
        days_since_last_publish=10,
        publish_cadence_variance=None
    )
    dri = calculate_dri(metric)
    assert dri == "insufficient data"

def test_analytics_asi_calculation():
    metric = PackageRiskMetric(
        package_name="npm/react",
        fork_spike_ratio=3.5,
        open_issues_delta=10
    )
    asi = calculate_asi(metric)
    assert isinstance(asi, float)
    assert asi == 8.0

def test_analytics_asi_insufficient_data():
    metric = PackageRiskMetric(
        package_name="npm/react",
        fork_spike_ratio=None,
        open_issues_delta=10
    )
    asi = calculate_asi(metric)
    assert asi == "insufficient data"
