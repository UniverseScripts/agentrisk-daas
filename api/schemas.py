from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Union

class PackageRiskMetricResponse(BaseModel):
    package_name: str
    timestamp: datetime
    commit_velocity_24h: int
    open_issues_delta: int
    fork_velocity_24h: int
    contributor_churn: float
    maintainer_count: int | None = None
    single_maintainer_flag: bool = False
    days_since_last_publish: int | None = None
    publish_cadence_variance: float | None = None
    fork_spike_ratio: float | None = None

    model_config = ConfigDict(from_attributes=True)

class AdvancedPackageRiskAnalyticsResponse(BaseModel):
    package_name: str
    timestamp: datetime
    
    # Composite Analytical Indices (can be float or "insufficient data" string)
    maintainer_concentration_index: Union[float, str]
    dormancy_reactivation_index: Union[float, str]
    anomalous_spike_index: Union[float, str]
    
    # Raw registry signals included for context
    maintainer_count: int | None = None
    single_maintainer_flag: bool = False
    days_since_last_publish: int | None = None
    publish_cadence_variance: float | None = None
    fork_spike_ratio: float | None = None

    model_config = ConfigDict(from_attributes=True)
