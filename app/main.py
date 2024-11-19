from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .database import Base, engine, get_db
from .crud import get_rate_by_date_and_cargo, create_rate
from .schemas import RateCreate, RateResponse

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/calculate/", response_model=float)
async def calculate_insurance_cost(cargo_type: str, declared_cost: float, date: str, db: AsyncSession = Depends(get_db)):
    rate = await get_rate_by_date_and_cargo(db, cargo_type, date)
    if not rate:
        raise HTTPException(status_code=404, detail="Rate not found")
    return declared_cost * rate.rate


@app.post("/rates/", response_model=RateResponse)
async def add_rate(rate: RateCreate, db: AsyncSession = Depends(get_db)):
    return await create_rate(db, rate)
