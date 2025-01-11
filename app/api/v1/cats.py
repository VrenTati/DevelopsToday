from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, Cat
import aiohttp

from core.config import settings
from core.schemas.cat_schema import CatBase, CatCreate, CatUpdate

router = APIRouter(prefix=settings.api.v1.cat)

async def validate_breed(breed: str):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.thecatapi.com/v1/breeds") as response:
            if response.status != 200:
                raise HTTPException(status_code=503, detail="Unable to validate breed")
            breeds = {b["name"] for b in await response.json()}
            if breed not in breeds:
                raise HTTPException(status_code=400, detail="Invalid breed")

@router.get("/", response_model=list[CatBase])
async def get_cats(
        db: AsyncSession = Depends(db_helper.session_getter),
):
    cats = await db.execute(select(Cat))

    return cats.scalars().all()

@router.get("/{cat_id}", response_model=CatBase)
async def get_cat(
        cat_id: int,
        db: AsyncSession = Depends(db_helper.session_getter),
):
    cat = await db.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat

@router.post("/", response_model=CatBase)
async def create_cat(
        cat: CatCreate,
        db: AsyncSession = Depends(db_helper.session_getter),
):
    await validate_breed(cat.breed)
    new_category = Cat(**cat.dict())
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)

    return new_category

@router.put("/{cat_id}", response_model=CatBase)
async def update_cat(
        cat_id: int,
        cat_data: CatUpdate,
        db: AsyncSession = Depends(db_helper.session_getter)
):
    cat = await db.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    for key, value in cat_data.dict(exclude_unset=True).items():
        setattr(cat, key, value)
    await db.commit()
    await db.refresh(cat)

    return cat

@router.delete("/{cat_id}")
async def delete_cat(
        cat_id: int,
        db: AsyncSession = Depends(db_helper.session_getter),
):
    cat = await db.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    await db.delete(cat)
    await db.commit()

    return {"detail": "Cat deleted"}
