from pydantic import BaseModel

class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str]
    is_complete: bool = False