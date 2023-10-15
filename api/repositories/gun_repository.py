
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_
from sqlalchemy.sql import select

from models.models import Gun
from models.schemas import GunCreate, GunFilter


class GunRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_guns(self):
        result = await self.session.execute(select(Gun))
        guns = result.scalars().all()
        return guns

    async def create_gun(self, gun: GunCreate):
        new_gun = Gun(**gun.model_dump())
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

    async def get_guns_by_caliber(self, caliber: str):
        try:
            result = await self.session.execute(select(Gun).where(Gun.caliber == caliber))
            guns_by_caliber = result.scalars().all()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Guns not found")
        return guns_by_caliber

    async def get_guns_by_barrel_type(self, barrel_type: str):
        try:
            result = await self.session.execute(select(Gun).where(Gun.barrel_type == barrel_type))
            guns_by_barrel_type = result.scalars().all()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Guns not found")
        return guns_by_barrel_type

    async def get_guns_by_name(self, names: str):
        try:
            query = select(Gun).where(or_(*[Gun.name.ilike(f"%{name}%") for name in names]))
            result = await self.session.execute(query)
            guns_by_name = result.scalars().all()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Guns not found")
        return guns_by_name

    async def get_guns_by_filters(
            self,
            gun_filter: GunFilter
    ) -> list:
        """
        Get guns by filters.

        Args:
            name: The gun name.
            caliber: The gun caliber.
            barrel_type: The gun barrel type.
            category_id: The gun category ID

        Returns:
            A list of guns.
            :param gun_filter:
        """

        query = select(Gun).where(gun_filter.get_filter_criteria())
        result = await self.session.execute(query)
        return result.scalars().all()
