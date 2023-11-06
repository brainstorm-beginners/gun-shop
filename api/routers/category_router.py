from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import get_current_user
from api.repositories.category_repository import CategoryRepository
from models.models import User, Category
from models.schemas import CategoryCreate, CategoryRead, CategoryUpdate
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


@router.get("/categories/{category_id}", response_model=CategoryRead)
async def get_category(category_id: int, session: AsyncSession = Depends(get_async_session)):
    category_repository = CategoryRepository(session)

    category = await category_repository.get_category(category_id)
    return category


@router.post("/categories/", response_model=CategoryCreate)
async def create_category(category: CategoryCreate, session: AsyncSession = Depends(get_async_session), current_user: User=Depends(get_current_user)):
    category_repository = CategoryRepository(session)

    categories = await category_repository.create_category(category)
    return categories


@router.delete("/categories/{category_id}", response_model=None)
async def delete_category(category_id: int, session: AsyncSession = Depends(get_async_session), current_user: User=Depends(get_current_user)):
    category_repository = CategoryRepository(session)

    category = await category_repository.delete_category(category_id)
    return None


@router.put("/categories/{category_id}", response_model=CategoryRead)
async def update_category(category_id: int, category: CategoryUpdate, session: AsyncSession = Depends(get_async_session), current_user: User=Depends(get_current_user)):
    category_repository = CategoryRepository(session)

    category = await category_repository.update_category(category_id, category)
    return category
