from sqlalchemy import Column, Integer, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class SatelliteIndex(Base):
    __tablename__ = "satellite_indices"

    id = Column(Integer, primary_key=True, index=True)
    vineyard_id = Column(Integer, ForeignKey('vineyards.id'))
    capture_date = Column(Date)
    ndvi_score = Column(Numeric(4, 3))
    moisture_index = Column(Numeric(4, 3))

    vineyard = relationship("Vineyard", back_populates="satellite_indices")