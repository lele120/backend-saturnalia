from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.services.vineyard_service import VineyardService

router = APIRouter(prefix="/vineyards", tags=["vineyards"])

@router.get("/area")
async def get_vineyard_area(code: str = Query(..., description="Vineyard code"), db: AsyncSession = Depends(get_db)):
    service = VineyardService(db)
    return await service.get_vineyard_area(code)

@router.get("/vigor")
async def get_vineyard_vigor(code: str = Query(..., description="Vineyard code"), db: AsyncSession = Depends(get_db)):
    service = VineyardService(db)
    return await service.get_vineyard_vigor(code)

@router.get("/prediction")
async def get_wine_prediction(code: str = Query(..., description="Vineyard code"), year: int = Query(..., description="Vintage year"), db: AsyncSession = Depends(get_db)):
    service = VineyardService(db)
    return await service.get_wine_prediction(code, year)