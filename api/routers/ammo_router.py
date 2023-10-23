from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.ammo_repository import AmmoRepository
from models.schemas import AmmoRead, AmmoCreate
from utils.database import get_async_session

router = APIRouter(
    tags=["Ammo"],
    prefix="/api"
)


@router.get("/ammo/", response_model=List[AmmoRead])
async def get_ammo(session: AsyncSession = Depends(get_async_session)):
    ammo_repository = AmmoRepository(session)

    ammo = await ammo_repository.get_ammo()
    return ammo


@router.post("/ammo/", response_model=AmmoCreate)
async def create_ammo(ammo: AmmoCreate, session: AsyncSession = Depends(get_async_session)):
    ammo_repository = AmmoRepository(session)

    new_ammo = await ammo_repository.create_ammo(ammo)
    return new_ammo


@router.get("/ammo/caliber/", response_model=List[AmmoRead])
async def get_amount_of_ammo_by_caliber(calibers: List[str] = Query(), session: AsyncSession = Depends(get_async_session)):
    ammo_repository = AmmoRepository(session)

    ammo_by_calibers = await ammo_repository.get_amount_of_ammo_by_caliber(calibers)
    return ammo_by_calibers
