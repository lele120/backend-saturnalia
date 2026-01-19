import logging
import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from geoalchemy2 import Geography
from app.models.vineyard import Vineyard
from app.models.satellite_index import SatelliteIndex
from app.models.wine_prediction import WinePrediction
from typing import Optional
from uuid import UUID
from cachetools import TTLCache

logger = logging.getLogger(__name__)

class VineyardRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.area_cache = TTLCache(maxsize=100, ttl=300)  # 5 min TTL
        self.vigor_cache = TTLCache(maxsize=100, ttl=300)
        self.prediction_cache = TTLCache(maxsize=100, ttl=300)

    async def get_vineyard_area(self, code: str):
        if code in self.area_cache:
            return self.area_cache[code]
        start_time = time.perf_counter()
        stmt = select(
            Vineyard.name,
            (func.ST_Area(Vineyard.boundary.cast(Geography())) / 10000).label("hectares")
        ).where(Vineyard.code == UUID(code))
        logger.info(f"Executing query: {stmt}")
        result = await self.db.execute(stmt)
        row = result.fetchone()
        elapsed = time.perf_counter() - start_time
        if elapsed > 1.0:  # Log if query takes more than 1 second
            logger.warning(f"Slow query in get_vineyard_area for code {code}: {elapsed:.2f}s")
        if row:
            self.area_cache[code] = row
        return row

    async def get_vineyard_vigor(self, code: str):
        if code in self.vigor_cache:
            return self.vigor_cache[code]
        start_time = time.perf_counter()
        stmt = select(
            Vineyard.name,
            func.avg(SatelliteIndex.ndvi_score).label("avg_vigor")
        ).join(SatelliteIndex).where(Vineyard.code == UUID(code)).group_by(Vineyard.name)
        logger.info(f"Executing query: {stmt}")
        result = await self.db.execute(stmt)
        row = result.fetchone()
        elapsed = time.perf_counter() - start_time
        if elapsed > 1.0:
            logger.warning(f"Slow query in get_vineyard_vigor for code {code}: {elapsed:.2f}s")
        if row:
            self.vigor_cache[code] = row
        return row

    async def get_wine_prediction(self, code: str, year: int) -> Optional[WinePrediction]:
        key = f"{code}_{year}"
        if key in self.prediction_cache:
            return self.prediction_cache[key]
        start_time = time.perf_counter()
        stmt = select(WinePrediction).join(Vineyard).where(
            Vineyard.code == UUID(code),
            WinePrediction.vintage_year == year
        )
        logger.info(f"Executing query: {stmt}")
        result = await self.db.execute(stmt)
        prediction = result.scalars().first()
        elapsed = time.perf_counter() - start_time
        if elapsed > 1.0:
            logger.warning(f"Slow query in get_wine_prediction for code {code}, year {year}: {elapsed:.2f}s")
        if prediction:
            self.prediction_cache[key] = prediction
        return prediction