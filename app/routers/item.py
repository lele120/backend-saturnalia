from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database.database import get_db
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    service = ItemService(db)
    return await service.create_item(item)

@router.get("/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 100, sort_by: Optional[str] = None, order: str = "asc", description_filter: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    service = ItemService(db)
    return await service.get_items(skip, limit, sort_by, order, description_filter)

@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    service = ItemService(db)
    item = await service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item_update: ItemUpdate, db: AsyncSession = Depends(get_db)):
    service = ItemService(db)
    item = await service.update_item(item_id, item_update)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.delete("/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    service = ItemService(db)
    item = await service.delete_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}