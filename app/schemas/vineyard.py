from pydantic import BaseModel, Field
from typing import Optional, Annotated

class VineyardAreaResponse(BaseModel):
    name: str
    hectares: float

class VineyardVigorResponse(BaseModel):
    name: str
    avg_vigor: float

class WinePredictionResponse(BaseModel):
    id: int
    vintage_year: int = Field(..., ge=1900, le=2100)
    quality_score: int
    market_price_est: float