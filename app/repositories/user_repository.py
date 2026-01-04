from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[UserModel, UserCreate, UserUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, UserModel)

    async def get_all(self, skip: int = 0, limit: int = 100):
        result = await self.db.execute(select(UserModel).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_by_id(self, user_id: int):
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        return result.scalars().first()

    async def create(self, user_data: UserCreate):
        user = UserModel(**user_data.model_dump())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user_id: int, user_data: UserUpdate):
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user = result.scalars().first()
        if user:
            for key, value in user_data.model_dump(exclude_unset=True).items():
                setattr(user, key, value)
            await self.db.commit()
            await self.db.refresh(user)
        return user

    async def delete(self, user_id: int):
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user = result.scalars().first()
        if user:
            await self.db.delete(user)
            await self.db.commit()
        return user