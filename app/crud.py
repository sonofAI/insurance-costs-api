from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Rate
from .schemas import RateCreate

async def get_rate_by_date_and_cargo(db: AsyncSession, cargo_type: str, date: str):
    result = await db.execute(
        select(Rate).where(Rate.cargo_type == cargo_type, Rate.date == date)
    )
    return result.scalars().first()

async def create_rate(db: AsyncSession, rate: RateCreate):
    db_rate = Rate(**rate.dict())
    db.add(db_rate)
    await db.commit()
    await db.refresh(db_rate)
    return db_rate
