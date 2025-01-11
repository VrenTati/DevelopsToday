from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Boolean, Float, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.id_int_pk_mixin import IdIntPKMixin

if TYPE_CHECKING:
    from .target import Target
    from .cat import Cat

class Mission(Base, IdIntPKMixin):
    cat_id: Mapped[int | None] = mapped_column(
        ForeignKey("cat.id", ondelete="SET NULL"), nullable=True
    )
    is_complete: Mapped[bool] = mapped_column(Boolean, default=False)

    cat: Mapped["Cat"] = relationship(
        "Cat", back_populates="missions"
    )
    targets: Mapped[list["Target"]] = relationship(
        "Target", back_populates="mission", cascade="all, delete", lazy="selectin"
    )