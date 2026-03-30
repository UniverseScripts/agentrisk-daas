from pydantic import BaseModel, ConfigDict
from datetime import datetime

class RepositoryMetricResponse(BaseModel):
    repo_name: str
    timestamp: datetime
    commit_velocity_24h: int
    open_issues_delta: int
    fork_velocity_24h: int
    contributor_churn: float

    model_config = ConfigDict(from_attributes=True)
