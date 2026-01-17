from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, asc, or_
from app.models.item import Item as ItemModel
from app.schemas.item import ItemCreate, ItemUpdate
from app.repositories.base_repository import BaseRepository
from typing import Optional

class ItemRepository(BaseRepository[ItemModel, ItemCreate, ItemUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, ItemModel)

    async def get_all(self, skip: int = 0, limit: int = 100, sort_by: Optional[str] = None, order: str = "asc", description_filter: Optional[str] = None):
        query = select(ItemModel)
        if description_filter:
            query = query.where(ItemModel.description.ilike(f"%{description_filter}%"))
        if sort_by:
            if sort_by == "name":
                column = ItemModel.name
            elif sort_by == "description":
                column = ItemModel.description
            else:
                column = ItemModel.id  # default
            direction = desc if order == "desc" else asc
            query = query.order_by(direction(column))
            print(f"SQL Query: {str(query)}") 
        result = await self.db.execute(query.offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_by_id(self, entity_id: int):
        result = await self.db.execute(select(ItemModel).where(ItemModel.id == entity_id))
        return result.scalars().first()

    async def create(self, entity_data: ItemCreate):
        item = ItemModel(**entity_data.model_dump())
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update(self, entity_id: int, entity_data: ItemUpdate):
        result = await self.db.execute(select(ItemModel).where(ItemModel.id == entity_id))
        item = result.scalars().first()
        if item:
            for key, value in entity_data.model_dump(exclude_unset=True).items():
                setattr(item, key, value)
            await self.db.commit()
            await self.db.refresh(item)
        return item

    async def delete(self, entity_id: int):
        result = await self.db.execute(select(ItemModel).where(ItemModel.id == entity_id))
        item = result.scalars().first()
        if item:
            await self.db.delete(item)
            await self.db.commit()
        return item