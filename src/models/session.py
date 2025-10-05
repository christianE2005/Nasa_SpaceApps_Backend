from typing import TYPE_CHECKING, Dict, Any
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, JSON, ForeignKey
from src.core.models import UUIDPrimaryKey, Timestamp
from src.core.database import Base

if TYPE_CHECKING:
    from .user import User

class Session(Base, UUIDPrimaryKey, Timestamp):
    __tablename__ = "sessions"

    parametros: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    csv_url: Mapped[str] = mapped_column(String(2048), nullable=False)

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="sessions",
    )
