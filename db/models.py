import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, DateTime, Boolean, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """Base class for SQLAlchemy 2.0 declarative models."""
    pass

class PackageRiskMetric(Base):
    """
    Time-series maintainer concentration and dormancy-reactivation metrics.
    Stores aggregated data with B-Tree indexes on temporal and package identifiers.
    """
    __tablename__ = 'package_risk_metrics'
    __table_args__ = (UniqueConstraint('package_name', 'timestamp', name='uix_package_time'),)

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    package_name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        index=True, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    commit_velocity_24h: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    open_issues_delta: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    fork_velocity_24h: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    # Formula: 1.0 - (unique_commit_authors_past_24h / total_commits_past_24h)
    contributor_churn: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # Real Metadata from npm/PyPI
    maintainer_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    single_maintainer_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    days_since_last_publish: Mapped[int | None] = mapped_column(Integer, nullable=True)
    publish_cadence_variance: Mapped[float | None] = mapped_column(Float, nullable=True)
    fork_spike_ratio: Mapped[float | None] = mapped_column(Float, nullable=True)


class APIKey(Base):
    """
    Client authentication and subscription ledger.
    id is a UUIDv4 string.
    valid_api_keys stores a SHA-256 hash of the raw API key for secure lookup.
    """
    __tablename__ = "api_key"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    valid_api_keys: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    subscription_id: Mapped[str | None] = mapped_column(String, unique=True, index=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
