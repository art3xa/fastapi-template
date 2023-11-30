import uuid

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class JWTToken(Base):
    __tablename__ = "jwt_tokens"

    jti: Mapped[str] = mapped_column(String(length=36), primary_key=True, index=True, nullable=False)
    is_blacklisted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="jwt_tokens")  # noqa: F821
    device_id: Mapped[str] = mapped_column(String(length=36), nullable=False)
