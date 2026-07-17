from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, ConfigDict
from app.config import Base

# =====================================================================
# 1. DATABASE ENTITY 
# =====================================================================
class UserEntity(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


# =====================================================================
# 2. DTO SCHEMAS (Modernized to Pydantic V2)
# =====================================================================

class UserRegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    # Modern Pydantic V2 way to read standard ORM objects cleanly without warnings
    model_config = ConfigDict(from_attributes=True)