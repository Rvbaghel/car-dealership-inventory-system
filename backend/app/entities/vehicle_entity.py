from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel
from app.config import Base

# SQLAlchemy Database Model Layer
class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

# Pydantic Structural Contracts
class VehicleCreateRequest(BaseModel):
    make: str
    model: str
    category: str
    price: float
    quantity: int

    class Config:
        from_attributes = True