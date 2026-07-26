from typing import Union
from db.models import PackageRiskMetric

def calculate_mci(metric: PackageRiskMetric) -> Union[float, str]:
    """
    Maintainer Concentration Index (MCI).
    High score = high bus-factor / takeover risk.
    Function of maintainer_count and contributor_churn.
    """
    if metric.maintainer_count is None:
        return "insufficient data"
    
    base_risk = 10.0 / max(1, metric.maintainer_count)
    churn_factor = 1.0 + metric.contributor_churn
    
    mci = base_risk * churn_factor
    return round(min(10.0, mci), 3)

def calculate_dri(metric: PackageRiskMetric) -> Union[float, str]:
    """
    Dormancy Reactivation Index (DRI).
    High score = package dormant on a stable historical cadence, then suddenly reactivated.
    Function of days_since_last_publish and publish_cadence_variance.
    """
    if metric.days_since_last_publish is None or metric.publish_cadence_variance is None:
        return "insufficient data"
        
    variance = max(1.0, metric.publish_cadence_variance)
    
    dri = (metric.days_since_last_publish / variance)
    return round(min(10.0, max(0.0, dri)), 3)

def calculate_asi(metric: PackageRiskMetric) -> Union[float, str]:
    """
    Anomalous Spike Index (ASI).
    Secondary, corroborating signal only — sudden fork/issue activity.
    Function of fork_spike_ratio and open_issues_delta.
    """
    if metric.fork_spike_ratio is None:
        return "insufficient data"
        
    spike_factor = metric.fork_spike_ratio
    issue_delta_factor = max(0, metric.open_issues_delta) * 0.1
    
    asi = spike_factor * 2.0 + issue_delta_factor
    return round(min(10.0, asi), 3)
