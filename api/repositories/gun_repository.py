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
        result = await self.session.execute(select(Gun))
        guns = result.scalars().all()
        return guns

    async def get_guns_by_caliber(self, caliber: str):
        try:
            result = await self.session.execute(select(Gun).where(Gun.caliber == caliber))
            guns = result.scalars().all()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Gun not found")
        return guns

    async def create_gun(self, gun: GunCreate):
        new_gun = Gun(**gun.dict())
        self.session.add(new_gun)
        await self.session.commit()
        await self.session.refresh(new_gun)
        return new_gun

    async def get_guns_by_category(self, category_id: int):
        try:
            result = await self.session.execute(select(Gun).where(Gun.category_id == category_id))
            guns_by_category = result.scalars().all()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Guns not found")
        return guns_by_category
