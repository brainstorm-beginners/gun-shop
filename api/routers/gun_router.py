from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.gun_repository import GunRepository
from models.schemas import Gun, GunCreate
from utils.database import get_async_session

router = APIRouter(
    tags=["Gun"],
    prefix="/api"
)


@router.get("/guns/", response_model=List[Gun])
async def get_guns(session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    guns = await gun_repository.get_guns()
    return guns


@router.get("/guns/{caliber}", response_model=List[Gun])
async def get_gun_by_caliber(caliber: str, session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    guns = await gun_repository.get_gun_by_caliber(caliber)
    return guns


@router.post("/guns/", response_model=Gun)
async def create_gun(gun: GunCreate, session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    new_gun = await gun_repository.create_gun(gun)
    return new_gun

