from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.category_repository import CategoryRepository
from models.schemas import CategoryCreate, CategoryRead
from utils.database import get_async_session

router = APIRouter(
    tags=["Category"],
    prefix="/api"
)


@router.get("/categories/", response_model=List[CategoryRead])
async def get_categories(session: AsyncSession = Depends(get_async_session)):
    category_repository = CategoryRepository(session)

    categories = await category_repository.get_categories()
    return categories


@router.post("/categories/", response_model=CategoryCreate)
async def create_category(category: CategoryCreate, session: AsyncSession = Depends(get_async_session)):
    category_repository = CategoryRepository(session)

    categories = await category_repository.create_category(category)
    return categories
