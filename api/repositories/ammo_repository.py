from typing import List

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Ammo
from models.schemas import AmmoCreate


class AmmoRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_ammo(self):
        result = await self.session.execute(select(Ammo))
        ammo = result.scalars().all()
        return ammo

    async def create_ammo(self, ammo: AmmoCreate):
        new_ammo = Ammo(**ammo.model_dump())
        self.session.add(new_ammo)
        await self.session.commit()
        await self.session.refresh(new_ammo)
        return new_ammo

    async def get_amount_of_ammo_by_caliber(self, calibers: List[str]):
        try:
            result = await self.session.execute(select(Ammo).where(or_(*[Ammo.calibers.ilike(f"%{caliber}%") for caliber in calibers])))
            ammo_by_calibers = result.scalars().all()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Ammo not found")
        return ammo_by_calibers
