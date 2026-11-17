from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, BigIntPK
from app.models.enums import UserRole


class User(Base):
    """Öğrenci ve danışman hesapları (FR-01, FR-07)."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    # NFR-01: şifre açık metin olarak tutulmaz, yalnızca hash saklanır.
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
