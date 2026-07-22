from pydantic import BaseModel, ConfigDict
from datetime import datetime

class RepositoryMetricResponse(BaseModel):
    repo_name: str
    timestamp: datetime
    commit_velocity_24h: int
    open_issues_delta: int
    fork_velocity_24h: int
    contributor_churn: float
    framework_shifts: str | None = None
    license_type: str | None = None
    license_drift: bool = False
    model_weight_formats: str | None = None
    fine_tuning_frameworks: str | None = None

    model_config = ConfigDict(from_attributes=True)


class AdvancedTechnographicAnalyticsResponse(BaseModel):
    repo_name: str
    timestamp: datetime
    
    # Composite Analytical Indices
    framework_migration_index: float
    contributor_flight_risk: float
    production_readiness_score: float
    license_liability_score: float
    
    # Raw AST Signals
    license_type: str | None = None
    license_drift: bool = False
    framework_shifts: str | None = None
    model_weight_formats: str | None = None
    fine_tuning_frameworks: str | None = None

    model_config = ConfigDict(from_attributes=True)
