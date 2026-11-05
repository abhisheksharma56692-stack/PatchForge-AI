"""Declarative base and common model mixins for SQLAlchemy."""
from datetime import datetime
from sqlalchemy import DateTime, Column
from sqlalchemy.orm import declarative_base, declared_attr

Base = declarative_base()


class TimestampMixin:
    """Provides created_at and updated_at datetime columns."""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

