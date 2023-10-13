from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Gun
from models.schemas import GunCreate


class GunRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_guns(self):
        guns = await self.session.execute(select(Gun))
        return guns.scalars().all()

    async def get_gun_by_caliber(self, caliber: str):
        try:
            gun = await self.session.execute(select(Gun).where(caliber == Gun.caliber))
            return gun.scalar_one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Gun not found")

    async def create_gun(self, gun: GunCreate):
        new_gun = Gun(**gun.dict())

        self.session.add(new_gun)
        await self.session.commit()
        await self.session.refresh(new_gun)

        return new_gun

