from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class IdIntPKMixin:
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
