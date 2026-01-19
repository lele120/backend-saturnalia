from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from geoalchemy2 import Geography
from app.models.vineyard import Vineyard
from app.models.satellite_index import SatelliteIndex
from app.models.wine_prediction import WinePrediction
from typing import Optional
from uuid import UUID

class VineyardRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_vineyard_area(self, code: str):
        stmt = select(
            Vineyard.name,
            (func.ST_Area(Vineyard.boundary.cast(Geography())) / 10000).label("hectares")
        ).where(Vineyard.code == UUID(code))
        result = await self.db.execute(stmt)
        return result.fetchone()

    async def get_vineyard_vigor(self, code: str):
        stmt = select(
            Vineyard.name,
            func.avg(SatelliteIndex.ndvi_score).label("avg_vigor")
        ).join(SatelliteIndex).where(Vineyard.code == UUID(code)).group_by(Vineyard.name)
        result = await self.db.execute(stmt)
        return result.fetchone()

    async def get_wine_prediction(self, code : str, year: int) -> Optional[WinePrediction]:
        stmt = select(WinePrediction).join(Vineyard).where(
            Vineyard.code == UUID(code),
            WinePrediction.vintage_year == year
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()