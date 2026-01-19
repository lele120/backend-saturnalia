from sqlalchemy import Column, Integer, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database.database import Base

class WinePrediction(Base):
    __tablename__ = "wine_predictions"

    id = Column(Integer, primary_key=True, index=True)
    vineyard_id = Column(Integer, ForeignKey('vineyards.id'))
    vintage_year = Column(Integer)
    quality_score = Column(Integer)
    market_price_est = Column(Numeric(10, 2))

    vineyard = relationship("Vineyard", back_populates="wine_predictions")

    __table_args__ = (
        CheckConstraint('quality_score BETWEEN 0 AND 100'),
    )