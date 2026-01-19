from pydantic import BaseModel
from typing import Optional

class VineyardAreaResponse(BaseModel):
    name: str
    hectares: float

class VineyardVigorResponse(BaseModel):
    name: str
    avg_vigor: float

class WinePredictionResponse(BaseModel):
    id: int
    vintage_year: int
    quality_score: int
    market_price_est: float