from fastapi import APIRouter

from core.config import settings

from .cats import router as cats_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(cats_router, tags=["cats"])
