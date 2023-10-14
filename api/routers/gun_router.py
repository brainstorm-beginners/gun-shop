from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.gun_repository import GunRepository
from models.schemas import GunCreate, GunRead
from utils.database import get_async_session

router = APIRouter(
    tags=["Gun"],
    prefix="/api"
)


@router.get("/guns/", response_model=List[GunRead])
async def get_guns(session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    guns = await gun_repository.get_guns()
    return guns


@router.get("/guns/{caliber}", response_model=List[GunRead])
async def get_gun_by_caliber(caliber: str, session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    guns = await gun_repository.get_guns_by_caliber(caliber)
    return guns


@router.post("/guns/", response_model=GunCreate)
async def create_gun(gun: GunCreate, session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    new_gun = await gun_repository.create_gun(gun)
    return new_gun


@router.get("/guns/{category_id}", response_model=List[GunRead])
async def get_gun_by_category(category_id: int, session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    guns_by_category = await gun_repository.get_guns_by_category(category_id)
    return guns_by_category


