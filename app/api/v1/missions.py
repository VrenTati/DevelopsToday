from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import db_helper, Mission, Target, Cat

from core.config import settings
from core.schemas.mission_schema import MissionBase, MissionCreate
from core.schemas.target_schema import TargetBase, TargetUpdate

router = APIRouter(prefix=settings.api.v1.mission)

@router.get("/", response_model=list[MissionBase])
async def get_missions(
        db: AsyncSession = Depends(db_helper.session_getter),
):
    result = await db.execute(select(Mission).options(selectinload(Mission.targets)))
    return result.scalars().all()

@router.get("/{mission_id}", response_model=MissionBase)
async def get_mission(
        mission_id: int,
        db: AsyncSession = Depends(db_helper.session_getter),
):
    mission = await db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission

@router.post("/", response_model=MissionBase)
async def create_mission(
        mission: MissionCreate,
        db: AsyncSession = Depends(db_helper.session_getter),
):
    result = await db.execute(select(Mission).filter(Mission.cat_id == mission.cat_id, Mission.is_complete == False))
    existing_mission = result.scalars().first()

    if existing_mission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This cat already has an unfinished mission.",
        )

    new_mission = Mission(is_complete=mission.is_complete, cat_id=mission.cat_id)
    db.add(new_mission)
    await db.commit()

    for target_data in mission.targets:
        target = Target(**target_data.dict(), mission_id=new_mission.id)
        db.add(target)
    await db.commit()

    await db.refresh(new_mission)

    return new_mission

@router.delete("/{mission_id}")
async def delete_mission(
        mission_id: int,
        db: AsyncSession = Depends(db_helper.session_getter),
):
    mission = await db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if mission.cat_id:
        raise HTTPException(status_code=400, detail="Cannot delete a mission assigned to a cat")
    await db.delete(mission)
    await db.commit()

    return {"detail": "Mission deleted"}

@router.patch("/{mission_id}/targets/{target_id}", response_model=TargetBase)
async def update_target(
        mission_id: int,
        target_id: int,
        target_data: TargetUpdate,
        db: AsyncSession = Depends(db_helper.session_getter),
):
    target = await db.get(Target, target_id)
    if not target or target.mission_id != mission_id:
        raise HTTPException(status_code=404, detail="Target not found")

    mission = await db.get(Mission, mission_id)
    if mission.is_complete or target.is_complete:
        raise HTTPException(status_code=400, detail="Cannot update completed mission or target")

    for key, value in target_data.dict(exclude_unset=True).items():
        setattr(target, key, value)
    await db.commit()
    await db.refresh(target)

    result = await db.execute(select(Target).filter(Target.mission_id == mission_id))
    targets = result.scalars().all()

    if all(t.is_complete for t in targets):
        mission.is_complete = True
        db.add(mission)
        await db.commit()
        await db.refresh(mission)

    return target


@router.put("/{mission_id}/assign_cat/{cat_id}", response_model=MissionBase)
async def assign_cat_to_mission(
        mission_id: int,
        cat_id: int,
        db: AsyncSession = Depends(db_helper.session_getter),
):
    mission = await db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    cat = await db.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    mission.cat_id = cat_id
    await db.commit()
    await db.refresh(mission)

    return mission
