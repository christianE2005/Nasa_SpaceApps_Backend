from typing import TYPE_CHECKING, List
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String
from src.core.models import UUIDPrimaryKey, Timestamp
from src.core.database import Base

if TYPE_CHECKING:
    from .session import Session

class User(Base, UUIDPrimaryKey, Timestamp):
    __tablename__ = "users"

    user_email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    sessions: Mapped[List["Session"]] = relationship(
        "Session",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
