from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page
from fastapi_pagination import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.gun_repository import GunRepository
from models.schemas import GunCreate, GunRead, GunFilter
from utils.database import get_async_session

router = APIRouter(
    tags=["Gun"],
    prefix="/api"
)


@router.get("/guns/", response_model=Page[List[GunRead]])
async def get_guns(session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    guns = await gun_repository.get_guns()
    return paginate(guns)


@router.get("/guns/caliber/{caliber}", response_model=Page[List[GunRead]])
async def get_guns_by_caliber(caliber: str, session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    guns = await gun_repository.get_guns_by_caliber(caliber)
    return paginate(guns)


@router.post("/guns/", response_model=GunCreate)
async def create_gun(gun: GunCreate, session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    new_gun = await gun_repository.create_gun(gun)
    return new_gun


@router.get("/guns/category/{category_id}", response_model=Page[List[GunRead]])
async def get_guns_by_category(category_id: int, session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    guns_by_category = await gun_repository.get_guns_by_category(category_id)
    return paginate(guns_by_category)


@router.get("/guns/barrel_type/{barrel_type}", response_model=Page[List[GunRead]])
async def get_guns_by_barrel_type(barrel_type: str, session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    guns_by_barrel_type = await gun_repository.get_guns_by_barrel_type(barrel_type)
    return paginate(guns_by_barrel_type)


@router.get("/guns/name/{name}", response_model=Page[List[GunRead]])
async def get_guns_by_name(name: str, session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    guns_by_name = await gun_repository.get_guns_by_name(name)
    return paginate(guns_by_name)


@router.get("/guns/by_filter/", response_model=Page[List[GunRead]])
async def get_guns_by_filter(
    session: AsyncSession = Depends(get_async_session),
    names: List[str] = Query(None),
    barrelTypes: List[str] = Query(None),
    calibers: List[str] = Query(None),
    categories: List[int] = Query(None)
) -> List[GunRead]:
    gun_filter = GunFilter(
        names=names,
        barrelTypes=barrelTypes,
        calibers=calibers,
        categories=categories
    )
    gun_repository = GunRepository(session)

    guns_by_filter = await gun_repository.get_guns_by_filters(gun_filter)
    return paginate(guns_by_filter)
