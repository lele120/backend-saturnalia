from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.vineyard_repository import VineyardRepository
from app.schemas.vineyard import VineyardAreaResponse, VineyardVigorResponse, WinePredictionResponse

class VineyardService:
    def __init__(self, db: AsyncSession):
        self.repository = VineyardRepository(db)

    async def get_vineyard_area(self, code: str) -> VineyardAreaResponse:
        row = await self.repository.get_vineyard_area(code)
        if not row:
            raise HTTPException(status_code=404, detail="Vineyard not found")
        return VineyardAreaResponse(name=row[0], hectares=float(row[1]))

    async def get_vineyard_vigor(self, code: str) -> VineyardVigorResponse:
        row = await self.repository.get_vineyard_vigor(code)
        if not row:
            raise HTTPException(status_code=404, detail="Vineyard or satellite data not found")
        return VineyardVigorResponse(name=row[0], avg_vigor=float(row[1]))

    async def get_wine_prediction(self, code: str, year: int) -> WinePredictionResponse:
        row = await self.repository.get_wine_prediction(code, year)
        if not row:
            raise HTTPException(status_code=404, detail="Wine prediction not found")
        return WinePredictionResponse(
            id=row.id,
            vintage_year=row.vintage_year,
            quality_score=row.quality_score,
            market_price_est=float(row.market_price_est)
        )