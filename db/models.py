import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, DateTime, Boolean, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """Base class for SQLAlchemy 2.0 declarative models."""
    pass

class RepositoryMetric(Base):
    """
    Time-series repository velocity metrics.
    Stores aggregated data with B-Tree indexes on temporal and repository identifiers.
    """
    __tablename__ = 'repository_metrics'
    __table_args__ = (UniqueConstraint('repo_name', 'timestamp', name='uix_repo_time'),)

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repo_name: Mapped[str] = mapped_column(String, index=True, nullable=False)
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

    # Technographic Signals (AST Dependency Shifts, License Tracking, Quantization Formats)
    framework_shifts: Mapped[str | None] = mapped_column(String, nullable=True)  # JSON representation of AST framework changes
    license_type: Mapped[str | None] = mapped_column(String, nullable=True)     # Detected SPDX license (e.g. Apache-2.0, AGPL-3.0)
    license_drift: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False) # Flag indicating license alterations
    model_weight_formats: Mapped[str | None] = mapped_column(String, nullable=True) # JSON list of weight formats (e.g. GGUF, AWQ, Safetensors)
    fine_tuning_frameworks: Mapped[str | None] = mapped_column(String, nullable=True) # JSON list of fine-tuning stacks (e.g. Unsloth, PEFT)


class APIKey(Base):
    """
    Client authentication and balance ledger.
    id is a UUIDv4 string.
    valid_api_keys stores a SHA-256 hash of the raw API key for secure lookup.
    """
    __tablename__ = 'api_key'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    valid_api_keys: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    token_balance: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
