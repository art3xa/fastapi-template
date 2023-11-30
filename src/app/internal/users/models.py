import uuid

from sqlalchemy import UUID, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, nullable=False, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(length=256), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=64), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    jwt_tokens: Mapped[list["JWTToken"]] = relationship(back_populates="user")  # noqa: F821
