from typing import List, Any, Coroutine, Sequence

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import get_current_user
from api.repositories.gun_repository import GunRepository
from models.models import Gun, User
from models.schemas import GunCreate, GunRead, GunFilter
from utils.database import get_async_session

router = APIRouter(
    tags=["Gun"],
    prefix="/api"
)


@router.get("/guns/", response_model=List[GunRead])
async def get_guns(session: AsyncSession = Depends(get_async_session), page: int = 1, page_size: int = 10):
    gun_repository = GunRepository(session)

    guns = await gun_repository.get_guns()

    # Pagination logic
    start = (page - 1) * page_size
    end = start + page_size

    return guns[start:end]


@router.get("/gun/{gun_id}", response_model=GunRead)
async def get_gun(gun_id: int, session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)
    gun = await gun_repository.get_gun(gun_id)
    return gun


@router.get("/guns/caliber/{caliber}", response_model=List[GunRead])
async def get_guns_by_caliber(caliber: str, session: AsyncSession = Depends(get_async_session), page: int = 1, page_size: int = 10):
    gun_repository = GunRepository(session)

    guns = await gun_repository.get_guns_by_caliber(caliber)

    # Pagination logic
    start = (page - 1) * page_size
    end = start + page_size

    return guns[start:end]


@router.post("/guns/", response_model=GunCreate)
async def create_gun(gun: GunCreate, session: AsyncSession = Depends(get_async_session)):
    gun_repository = GunRepository(session)

    new_gun = await gun_repository.create_gun(gun)
    return new_gun


@router.get("/guns/category/{category_id}", response_model=List[GunRead])
async def get_guns_by_category(category_id: int, session: AsyncSession = Depends(get_async_session), current_user: User=Depends(get_current_user), page: int = 1, page_size: int = 10):
    gun_repository = GunRepository(session)

    guns_by_category = await gun_repository.get_guns_by_category(category_id)

    # Pagination logic
    start = (page - 1) * page_size
    end = start + page_size

    return guns_by_category[start:end]


@router.get("/guns/barrel_type/{barrel_type}", response_model=List[GunRead])
async def get_guns_by_barrel_type(barrel_type: str, session: AsyncSession = Depends(get_async_session), page: int = 1, page_size: int = 10):
    gun_repository = GunRepository(session)

    guns_by_barrel_type = await gun_repository.get_guns_by_barrel_type(barrel_type)

    # Pagination logic
    start = (page - 1) * page_size
    end = start + page_size

    return guns_by_barrel_type[start:end]


@router.get("/guns/name/{name}", response_model=List[GunRead])
async def get_guns_by_name(name: str, session: AsyncSession = Depends(get_async_session), page: int = 1, page_size: int = 10):
    gun_repository = GunRepository(session)

    guns_by_name = await gun_repository.get_guns_by_name(name)

    # Pagination logic
    start = (page - 1) * page_size
    end = start + page_size

    return guns_by_name[start:end]


@router.get("/guns/by_filter/", response_model=List[GunRead])
async def get_guns_by_filter(
    session: AsyncSession = Depends(get_async_session),
    names: List[str] = Query(None),
    barrelTypes: List[str] = Query(None),
    calibers: List[str] = Query(None),
    categories: List[int] = Query(None),
    page: int = 1,
    page_size: int = 10
) -> Sequence[Gun]:
    gun_filter = GunFilter(
        names=names,
        barrelTypes=barrelTypes,
        calibers=calibers,
        categories=categories
    )
    gun_repository = GunRepository(session)

    guns_by_filter = await gun_repository.get_guns_by_filters(gun_filter)

    # Pagination logic
    start = (page - 1) * page_size
    end = start + page_size

    return guns_by_filter[start:end]
