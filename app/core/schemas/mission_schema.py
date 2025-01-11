from pydantic import BaseModel
from typing import List, Optional

from core.schemas.target_schema import TargetBase, TargetCreate

class MissionBase(BaseModel):
    is_complete: bool = False
    targets: List[TargetBase]
    cat_id: Optional[int]

class MissionCreate(BaseModel):
    cat_id: Optional[int] = None
    is_complete: bool = False
    targets: List[TargetCreate]