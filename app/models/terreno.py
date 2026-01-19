from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

# Tabella associazione molti-a-molti tra terreni e cadastral_parcels
terreno_cadastral_association = Table(
    'terreno_particelle_association', Base.metadata,
    Column('terreno_id', Integer, ForeignKey('terreni.id'), primary_key=True),
    Column('cadastral_parcel_id', Integer, ForeignKey('cadastral_parcels.id'), primary_key=True),
)

class CadastralParcel(Base):
    __tablename__ = "cadastral_parcels"

    id = Column(Integer, primary_key=True, index=True)
    codice_comune = Column(String(100), nullable=False)
    nome_comune = Column(String(100), nullable=False)
    provincia = Column(String(2), nullable=False)
    regione = Column(String(100), nullable=False)
    sezione = Column(String(10), nullable=False, default="")
    foglio = Column(Integer, nullable=False)
    particella = Column(Integer, nullable=False)
    area_m2 = Column(Float, nullable=False)
    codice_istat = Column(String(6), nullable=False)
    data_inserimento = Column(String(20), nullable=False)

    # Relazione molti-a-molti con terreni
    terreni = relationship("Terreno", secondary=terreno_cadastral_association, back_populates="cadastral_parcels")

class Terreno(Base):
    __tablename__ = "terreni"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    comune = Column(String(100), nullable=False)
    area_coltivata_m2 = Column(Float, nullable=False)
    superficie_catastale_totale = Column(Float, nullable=False)

    # Relazione molti-a-molti con cadastral_parcels
    cadastral_parcels = relationship("CadastralParcel", secondary=terreno_cadastral_association, back_populates="terreni")