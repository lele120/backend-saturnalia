from sqlalchemy import Column, Integer, String, Text, Numeric
from app.database.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(Text)
    price = Column(Numeric(10, 2))