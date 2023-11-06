from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from api.repositories.auth_repository import AuthRepository

from api.auth import create_access_token, hash_password, get_current_user
from models.schemas import User, Token, UserRead
from utils.database import get_async_session
from utils.db_config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    tags=["Users"],
    prefix="/auth"
)


@router.get("/users/{username}", response_model=UserRead)
async def get_user_by_username(username: str, session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    auth_repository = AuthRepository(session)

    user = await auth_repository.get_user_by_username(username)
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 session: AsyncSession = Depends(get_async_session)):
    auth_repository = AuthRepository(session)

    user = await auth_repository.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=User)
async def register_user(user: User, session: AsyncSession = Depends(get_async_session),
                        current_user: User = Depends(get_current_user)):
    auth_repository = AuthRepository(session)
    db_user = await auth_repository.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    user.hashed_password = hash_password(user.hashed_password)
    return await auth_repository.create_user(user)
