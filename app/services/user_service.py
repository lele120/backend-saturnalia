from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User as UserModel
from typing import List

class UserService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[UserModel]:
        try:
            return await self.repository.get_all(skip, limit)
        except Exception as e:
            raise HTTPException(500, f"Error retrieving users: {str(e)}")

    async def get_user(self, user_id: int) -> UserModel | None:
        if user_id <= 0:
            raise HTTPException(400, "Invalid user ID")
        try:
            return await self.repository.get_by_id(user_id)
        except Exception as e:
            raise HTTPException(500, f"Error retrieving user: {str(e)}")

    async def create_user(self, user: UserCreate) -> UserModel:
        # Business logic: ensure email is valid and unique (DB handles unique)
        if not user.email.strip():
            raise HTTPException(400, "Email cannot be empty")
        try:
            return await self.repository.create(user)
        except IntegrityError:
            raise HTTPException(400, "User with this email already exists")
        except Exception as e:
            raise HTTPException(500, f"Error creating user: {str(e)}")

    async def update_user(self, user_id: int, user_update: UserUpdate) -> UserModel | None:
        if user_id <= 0:
            raise HTTPException(400, "Invalid user ID")
        try:
            return await self.repository.update(user_id, user_update)
        except IntegrityError:
            raise HTTPException(400, "Update violates constraints")
        except Exception as e:
            raise HTTPException(500, f"Error updating user: {str(e)}")

    async def delete_user(self, user_id: int) -> UserModel | None:
        if user_id <= 0:
            raise HTTPException(400, "Invalid user ID")
        try:
            return await self.repository.delete(user_id)
        except Exception as e:
            raise HTTPException(500, f"Error deleting user: {str(e)}")