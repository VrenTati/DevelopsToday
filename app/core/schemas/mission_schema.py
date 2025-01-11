from pydantic import BaseModel

class MissionBase(BaseModel):
    is_complete: bool = False
    targets: List[TargetBase]

class MissionCreate(MissionBase):
    cat_id: Optional[int]