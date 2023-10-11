from sqlalchemy.orm import DeclarativeBase

from src.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
