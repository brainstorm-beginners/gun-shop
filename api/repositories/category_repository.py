from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.models import Category
from models.schemas import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_categories(self):
        result = await self.session.execute(select(Category))
        categories = result.scalars().all()
        return categories

    async def get_category(self, category_id: int):
        result = await self.session.execute(select(Category).where(Category.id == category_id))
        category = result.scalar_one()
        return category

    async def get_category_by_name(self, name: str):
        try:
            result = await self.session.execute(select(Category).where(Category.name == name))
            category = result.scalar_one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    async def create_category(self, category: CategoryCreate):
        new_category = Category(**category.dict())
        self.session.add(new_category)
        await self.session.commit()
        await self.session.refresh(new_category)
        return new_category

    async def delete_category(self, category_id: int):
        category = await self.get_category(category_id)

        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        await self.session.delete(category)
        await self.session.commit()
        return category

    async def update_category(self, category_id: int, category: CategoryUpdate):
        category = await self.get_category(category_id)

        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        category.update_fields(**category.dict())

        await self.session.commit()
        await self.session.refresh(category)
        return category


