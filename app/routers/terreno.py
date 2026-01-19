from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Optional
from app.database.database import get_db
from app.services.terreno_service import TerrenoService
from app.repositories.terreno_repository import TerrenoRepository

router = APIRouter(prefix="/terreni", tags=["terreni"])

class ParticellaInput(BaseModel):
    comune: str
    sezione: Optional[str] = ""
    foglio: int
    particella: int

class TerrenoCreate(BaseModel):
    nome: str
    area_coltivata_m2: float
    particelle: List[ParticellaInput]

@router.post("/")
async def create_terreno(terreno: TerrenoCreate, db: AsyncSession = Depends(get_db)):
    service = TerrenoService(db)
    return await service.create_terreno(
        terreno.nome, 
        terreno.area_coltivata_m2, 
        [p.model_dump() for p in terreno.particelle]
    )

@router.get("/")
async def get_terreni(db: AsyncSession = Depends(get_db)):
    service = TerrenoService(db)
    return await service.get_terreni()

@router.get("/comuni")
async def get_comuni(db: AsyncSession = Depends(get_db)):
    """Restituisce lista comuni disponibili per autocompletamento"""

    service = TerrenoService(db)
    return {"comuni": await service.get_comuni()}

@router.get("/particelle")
async def lookup_particella(
    comune: str,
    sezione: Optional[str] = "",
    foglio: Optional[int] = None,
    particella: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Lookup particella catastale (opzionale ma utile per UX)"""
    if not comune or foglio is None or particella is None:
        raise HTTPException(400, "Specifica comune, foglio e particella per la ricerca")
    
    service = TerrenoService(db)
    p = await service.get_cadastral_parcel(comune, sezione, foglio, particella)
    if not p:
        raise HTTPException(404, "Particella non trovata nel catasto")
    return {
        "comune": p.nome_comune,
        "id": p.id,
        "codice": p.codice_comune,
        "sezione": p.sezione,
        "foglio": p.foglio,
        "particella": p.particella,
        "superficie_m2": p.area_m2
    }