from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.database.database import Base
import uuid

class Vineyard(Base):
    __tablename__ = "vineyards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    region = Column(String(50))
    boundary = Column(Geometry('POLYGON', srid=4326))
    code = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)

    satellite_indices = relationship("SatelliteIndex", back_populates="vineyard")
    wine_predictions = relationship("WinePrediction", back_populates="vineyard")