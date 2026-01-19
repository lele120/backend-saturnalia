from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.terreno_repository import TerrenoRepository
from app.models.terreno import CadastralParcel
from typing import List, Dict, Tuple

class TerrenoService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = TerrenoRepository(db)

    async def create_terreno(self, nome: str, area_coltivata_m2: float, particelle: List[Dict]) -> Dict:
        # Validazione: almeno una particella
        if not particelle:
            raise HTTPException(400, {
                "error": "PARTICELLE_MINIME",
                "message": "Devi specificare almeno una particella catastale",
                "details": "Un terreno deve essere associato ad almeno una particella"
            })

        comune_ref = None
        superficie_totale = 0.0
        cadastral_parcels = []
        particelle_univoche = set()
        particelle_dettagli = []

        for p in particelle:
            comune = p["comune"]
            sezione = p.get("sezione", "")
            foglio = p["foglio"]
            particella = p["particella"]

            # Validazione: particella esiste
            cadastral_parcel = await self.repository.get_cadastral_parcel(comune, sezione, foglio, particella)
            if not cadastral_parcel:
                raise HTTPException(400, {
                    "error": "PARTICELLA_NON_ESISTENTE",
                    "message": f"Particella {comune}/{sezione}/{foglio}/{particella} non trovata nel catasto",
                    "details": "Verifica i dati inseriti o contatta il supporto"
                })

            # Validazione: stesso comune
            if comune_ref is None:
                comune_ref = comune
            elif comune_ref != comune:
                raise HTTPException(400, {
                    "error": "COMUNE_DIVERSO",
                    "message": "Le particelle di uno stesso terreno devono appartenere allo stesso comune",
                    "details": f"Comune di riferimento: {comune_ref}. Rimuovi particelle di comuni diversi."
                })

            # Validazione: no duplicati nella richiesta
            key = (comune, sezione, foglio, particella)
            if key in particelle_univoche:
                raise HTTPException(400, {
                    "error": "PARTICELLA_DUPLICATA",
                    "message": f"Particella {comune}/{sezione}/{foglio}/{particella} duplicata nella richiesta",
                    "details": "Rimuovi i duplicati"
                })
            particelle_univoche.add(key)

            superficie_totale += cadastral_parcel.superficie_m2
            cadastral_parcels.append(cadastral_parcel)
            particelle_dettagli.append({
                "id": cadastral_parcel.id,
                "comune": comune,
                "sezione": sezione,
                "foglio": foglio,
                "particella": particella,
                "superficie_m2": cadastral_parcel.superficie_m2
            })

        # Validazione: area coltivata <= superficie totale
        if area_coltivata_m2 > superficie_totale:
            raise HTTPException(400, {
                "error": "AREA_SUPERIORE",
                "message": f"Area coltivata ({area_coltivata_m2} m²) supera la superficie catastale totale ({superficie_totale} m²)",
                "details": f"Riduci l'area coltivata o aggiungi più particelle. Massimo consentito: {superficie_totale} m²"
            })

        # Crea terreno con associazioni
        terreno_data = {
            "nome": nome,
            "comune": comune_ref,
            "area_coltivata_m2": area_coltivata_m2,
            "superficie_catastale_totale": superficie_totale,
            "cadastral_parcels": cadastral_parcels
        }

        terreno = await self.repository.create_terreno(terreno_data)

        return {
            "id": terreno.id,
            "nome": terreno.nome,
            "comune": terreno.comune,
            "area_coltivata_m2": terreno.area_coltivata_m2,
            "superficie_catastale_totale": terreno.superficie_catastale_totale,
            "particelle": particelle_dettagli
        }

    async def get_terreni(self) -> List[Dict]:
        terreni = await self.repository.get_all_terreni()
        result = []
        for t in terreni:
            # Conta particelle per terreno
            particelle_count = await self._count_particelle(t.id)
            result.append({
                "id": t.id,
                "nome": t.nome,
                "comune": t.comune,
                "area_coltivata_m2": t.area_coltivata_m2,
                "superficie_catastale_totale": t.superficie_catastale_totale,
                "numero_particelle": particelle_count
            })
        return result

    async def _count_particelle(self, terreno_id: int) -> int:
        """Conta particelle per terreno"""
        from sqlalchemy import select, func
        from app.models.terreno import terreno_cadastral_association

        stmt = select(func.count()).where(terreno_cadastral_association.c.terreno_id == terreno_id)
        result = await self.db.execute(stmt)
        count = result.scalar()
        return count if count is not None else 0
    
    async def get_comuni(self) -> List[Dict[str, str]]:
        """Ottiene lista di comuni unici dalle particelle catastali"""
        comuni_tuples = await self.repository.get_comuni()
        return [{"value": codice, "label": nome} for nome, codice in comuni_tuples]
    

    async def get_cadastral_parcel(self, comune: str, sezione: str, foglio: int, particella: int) -> CadastralParcel | None:
        return await self.repository.get_cadastral_parcel(comune, sezione, foglio, particella)