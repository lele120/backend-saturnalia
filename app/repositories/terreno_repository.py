from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from sqlalchemy.orm import joinedload
from app.models.terreno import Terreno, CadastralParcel
from typing import List, Tuple

class TerrenoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_terreno(self, terreno_data: dict):
        cadastral_parcels = terreno_data.pop("cadastral_parcels", [])
        terreno = Terreno(**terreno_data)
        terreno.cadastral_parcels.extend(cadastral_parcels)
        self.db.add(terreno)
        await self.db.commit()
        await self.db.refresh(terreno)
        return terreno

    async def get_all_terreni(self) -> List[Terreno]:
        result = await self.db.execute(select(Terreno))
        return list(result.scalars().all())

    async def get_terreno_by_id(self, terreno_id: int) -> Terreno | None:
        result = await self.db.execute(select(Terreno).where(Terreno.id == terreno_id))
        return result.scalars().first()

    async def get_cadastral_parcel(self, comune: str, sezione: str, foglio: int, particella: int) -> CadastralParcel | None:
        """Ottiene una particella catastale dal database"""
        # Se comune è codice_comune, cerca per codice, altrimenti per nome
        conditions = [
            (CadastralParcel.codice_comune == comune) | (CadastralParcel.nome_comune == comune),
            CadastralParcel.foglio == foglio,
            CadastralParcel.particella == particella
        ]
        if sezione:  # Se sezione è fornita e non vuota, aggiungila al where
            conditions.append(CadastralParcel.sezione == sezione)
        stmt = select(CadastralParcel).where(*conditions)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    
    async def get_comuni(self) -> List[Tuple[str, str]]:
        """Ottiene lista di comuni unici dalle particelle catastali"""
        stmt = select(CadastralParcel.nome_comune, CadastralParcel.codice_comune).distinct().order_by(CadastralParcel.nome_comune)
        result = await self.db.execute(stmt)
        return [(row[0], row[1]) for row in result.fetchall()]