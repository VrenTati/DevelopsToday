from pydantic import BaseModel, Field, validator, field_validator, root_validator, model_validator
from fastapi import HTTPException
from typing import Optional

class CatBase(BaseModel):
    name: str
    years_of_experience: int = Field(..., ge=0)
    breed: str
    salary: float = Field(..., ge=0)

class CatCreate(CatBase):
    pass

class CatUpdate(BaseModel):
    salary: Optional[float] = Field(..., ge=0)
