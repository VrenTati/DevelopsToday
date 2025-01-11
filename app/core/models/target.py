from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Boolean, Float, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.id_int_pk_mixin import IdIntPKMixin

if TYPE_CHECKING:
    from .mission import Mission

class Target(Base, IdIntPKMixin):
    mission_id: Mapped[int] = mapped_column(
        ForeignKey("mission.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_complete: Mapped[bool] = mapped_column(Boolean, default=False)

    mission: Mapped["Mission"] = relationship(
        "Mission", back_populates="targets"
    )