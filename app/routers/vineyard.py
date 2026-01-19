from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.services.vineyard_service import VineyardService

router = APIRouter(prefix="/vineyards", tags=["vineyards"])

@router.get(
    "/area",
    summary="Get Vineyard Area",
    description="Calculate and return the area of a vineyard in hectares using PostGIS ST_Area function.",
    responses={
        200: {
            "description": "Successful response with vineyard name and area",
            "content": {
                "application/json": {
                    "example": {"name": "Château Sample", "hectares": 87.92}
                }
            }
        },
        404: {"description": "Vineyard not found"},
        429: {"description": "Too many requests"}
    }
)
async def get_vineyard_area(
    code: str = Query(..., description="Unique UUID code of the vineyard", example="00e885e1-617f-4f97-99a6-ad4e59d30d55"),
    db: AsyncSession = Depends(get_db)
):
    service = VineyardService(db)
    return await service.get_vineyard_area(code)

@router.get(
    "/vigor",
    summary="Get Vineyard Vigor",
    description="Calculate average NDVI (Normalized Difference Vegetation Index) score for vineyard vigor assessment.",
    responses={
        200: {
            "description": "Successful response with average vigor",
            "content": {
                "application/json": {
                    "example": {"name": "Château Sample", "avg_vigor": 0.615}
                }
            }
        },
        404: {"description": "Vineyard or satellite data not found"},
        429: {"description": "Too many requests"}
    }
)
async def get_vineyard_vigor(
    code: str = Query(..., description="Unique UUID code of the vineyard", example="00e885e1-617f-4f97-99a6-ad4e59d30d55"),
    db: AsyncSession = Depends(get_db)
):
    service = VineyardService(db)
    return await service.get_vineyard_vigor(code)

@router.get(
    "/prediction",
    summary="Get Wine Prediction",
    description="Retrieve wine quality prediction and market price estimate for a specific vineyard and vintage year.",
    responses={
        200: {
            "description": "Successful response with prediction details",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "vintage_year": 2025,
                        "quality_score": 94,
                        "market_price_est": 120.5
                    }
                }
            }
        },
        404: {"description": "Wine prediction not found"},
        429: {"description": "Too many requests"}
    }
)
async def get_wine_prediction(
    code: str = Query(..., description="Unique UUID code of the vineyard", example="00e885e1-617f-4f97-99a6-ad4e59d30d55"),
    year: int = Query(..., description="Vintage year for the prediction", ge=1900, le=2100, example=2025),
    db: AsyncSession = Depends(get_db)
):
    service = VineyardService(db)
    return await service.get_wine_prediction(code, year)