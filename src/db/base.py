from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """Base for all models."""

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Return the table name for the model."""
        return f"{cls.__name__.lower()}"
