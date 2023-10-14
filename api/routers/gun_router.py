from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.gun_repository import GunRepository
from models.schemas import GunCreate, GunRead
from utils.database import get_async_session
from typing import Optional

router = APIRouter(
    tags=["Gun"],
    prefix="/api"
)


@router.get("/guns/", response_model=List[GunRead])
async def get_guns(session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    guns = await gun_repository.get_guns()
    return guns


@router.get("/guns/caliber/{caliber}", response_model=List[GunRead])
async def get_guns_by_caliber(caliber: str, session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    guns = await gun_repository.get_guns_by_caliber(caliber)
    return guns


@router.post("/guns/", response_model=GunCreate)
async def create_gun(gun: GunCreate, session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    new_gun = await gun_repository.create_gun(gun)
    return new_gun


@router.get("/guns/category/{category_id}", response_model=List[GunRead])
async def get_guns_by_category(category_id: int, session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    guns_by_category = await gun_repository.get_guns_by_category(category_id)
    return guns_by_category


@router.get("/guns/barrel_type/{barrel_type}", response_model=List[GunRead])
async def get_guns_by_category(barrel_type: str, session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    guns_by_barrel_type = await gun_repository.get_guns_by_barrel_type(barrel_type)
    return guns_by_barrel_type


@router.get("/guns/name/{name}", response_model=List[GunRead])
async def get_guns_by_name(name: str, session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    guns_by_name = await gun_repository.get_guns_by_name(name)
    return guns_by_name

@router.get("/guns/search", response_model=List[GunRead])
async def search_guns(
        name: Optional[str] = None,
        barrel_type: Optional[str] = None,
        category_id: Optional[int] = None,
        caliber: Optional[str] = None,
        session: AsyncSession = Depends(get_async_session)
):
    gun_repository = GunRepository(session)

    filters = {}
    if name:
        filters['name'] = name
    if caliber:
        filters['caliber'] = caliber
    if barrel_type:
        filters['barrel_type'] = barrel_type
    if category_id:
        filters['category_id'] = category_id

    guns = await gun_repository.filter_guns(filters)
    return guns

