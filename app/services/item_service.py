from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.repositories.item_repository import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate
from app.models.item import Item as ItemModel
from typing import List

class ItemService:
    def __init__(self, db: AsyncSession):
        self.repository = ItemRepository(db)

    async def get_items(self, skip: int = 0, limit: int = 100) -> List[ItemModel]:
        try:
            return await self.repository.get_all(skip, limit)
        except Exception as e:
            raise HTTPException(500, f"Error retrieving items: {str(e)}")

    async def get_item(self, item_id: int) -> ItemModel | None:
        if item_id <= 0:
            raise HTTPException(400, "Invalid item ID")
        try:
            return await self.repository.get_by_id(item_id)
        except Exception as e:
            raise HTTPException(500, f"Error retrieving item: {str(e)}")

    async def create_item(self, item: ItemCreate) -> ItemModel:
        # Business logic: ensure name is not empty
        if not item.name.strip():
            raise HTTPException(400, "Item name cannot be empty")
        try:
            return await self.repository.create(item)
        except IntegrityError:
            raise HTTPException(400, "Item with this name already exists")
        except Exception as e:
            raise HTTPException(500, f"Error creating item: {str(e)}")

    async def update_item(self, item_id: int, item_update: ItemUpdate) -> ItemModel | None:
        if item_id <= 0:
            raise HTTPException(400, "Invalid item ID")
        # Business logic: validate update data
        if item_update.name is not None and not item_update.name.strip():
            raise HTTPException(400, "Item name cannot be empty")
        try:
            return await self.repository.update(item_id, item_update)
        except IntegrityError:
            raise HTTPException(400, "Update violates constraints")
        except Exception as e:
            raise HTTPException(500, f"Error updating item: {str(e)}")

    async def delete_item(self, item_id: int) -> ItemModel | None:
        if item_id <= 0:
            raise HTTPException(400, "Invalid item ID")
        try:
            return await self.repository.delete(item_id)
        except Exception as e:
            raise HTTPException(500, f"Error deleting item: {str(e)}")

   