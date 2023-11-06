from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import User
from models.schemas import User as UserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user_by_username(self, username: str):
        result = await self.session.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        return user

    async def create_user(self, user: UserSchema):
        db_user = User(**user.model_dump())
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def authenticate_user(self, username: str, password: str):
        user_repository = AuthRepository(self.session)
        user = await user_repository.get_user_by_username(username)
        if not user or not pwd_context.verify(password, user.hashed_password):
            return False
        if user.is_admin:
            return user
