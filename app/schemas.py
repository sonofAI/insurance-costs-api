from pydantic import BaseModel
from datetime import date

class RateBase(BaseModel):
    cargo_type: str
    rate: float
    date: date

class RateCreate(RateBase):
    pass

class RateResponse(BaseModel):
    cargo_type: str
    rate: float
    date: date

    class Config:
        orm_mode = True
