from pydantic import BaseModel, Field, validator
from fastapi import HTTPException
import requests
from typing import Optional


async def validate_breed(breed: str):
    response = requests.get("https://api.thecatapi.com/v1/breeds")
    if response.status_code != 200:
        raise HTTPException(status_code=503, detail="Unable to validate breed")
    breeds = {b["name"] for b in response.json()}
    if breed not in breeds:
        raise HTTPException(status_code=400, detail="Invalid breed")

class CatBase(BaseModel):
    name: str
    years_of_experience: int = Field(..., ge=0)
    breed: str
    salary: float = Field(..., ge=0)

    @validator("breed")
    def check_breed(cls, v):
        validate_breed(v)
        return v

class CatCreate(CatBase):
    pass

class CatUpdate(BaseModel):
    salary: Optional[float] = Field(..., ge=0)