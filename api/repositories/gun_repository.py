from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query
from sqlalchemy import or_

from models.models import Gun
from models.schemas import GunCreate


class GunRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_guns(self):
        result = await self.session.execute(select(Gun))
        guns = result.scalars().all()
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

    async def filter_guns(self, filters: dict):
        try:
            query = Query(Gun)

            filter_list = []

            for key, value in filters.items():
                if key == 'name':
                    clean_values = [value.strip().replace(' ', '') for value in value.split(',')]
                    name_filters = [func.replace(Gun.name, ' ', '').ilike(f"%{value.lower()}%") for value in clean_values]
                    filter_list.extend(name_filters)
                elif key == 'barrel_type':
                    filter_list.append(Gun.barrel_type.in_(value))
                elif key == 'caliber':
                    caliber_values = [caliber.strip() for caliber in value.split(',')]
                    caliber_filters = [Gun.caliber == caliber for caliber in caliber_values]
                    filter_list.extend(caliber_filters)
                elif key == 'category_id':
                    category_ids_list = value.split(',')

                    category_ids_int = []
                    for category_id in category_ids_list:
                        try:
                            category_id_int = int(category_id)
                            category_ids_int.append(category_id_int)
                        except ValueError:
                            raise HTTPException(status_code=400, detail=f"Invalid category ID: {category_id}")

                    if not category_ids_int:
                        raise HTTPException(status_code=400, detail="Category IDs are empty")

                    category_filters = [Gun.category_id == category_id for category_id in category_ids_int]
                    filter_list.extend(category_filters)

            query = query.filter(or_(*filter_list))

            result = await self.session.execute(query)
            guns = result.scalars().all()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Guns not found")
        return guns
