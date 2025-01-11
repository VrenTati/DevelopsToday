from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Boolean, Float, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.id_int_pk_mixin import IdIntPKMixin

if TYPE_CHECKING:
    from .mission import Mission


class Cat(Base, IdIntPKMixin):
    name: Mapped[str] = mapped_column(String, nullable=False)
    years_of_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    breed: Mapped[str] = mapped_column(String, nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False)

    missions: Mapped[list["Mission"]] = relationship(
        "Mission", back_populates="cat", lazy="selectin"
    )
