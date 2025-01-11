from pydantic import BaseModel
from typing import List, Optional

class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str]
    is_complete: bool = False

class TargetCreate(BaseModel):
    name: str
    country: str
    notes: Optional[str] = None
    is_complete: bool = False

    class Config:
        orm_mode = True

class TargetUpdate(BaseModel):
    notes: Optional[str]
    is_complete: Optional[bool]

    class Config:
        orm_mode = True
