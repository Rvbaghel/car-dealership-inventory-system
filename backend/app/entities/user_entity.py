from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from app.config import Base

# =====================================================================
# 1. DATABASE ENTITY (The Java JPA @Entity equivalent)
# =====================================================================
class UserEntity(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


# =====================================================================
# 2. DTO SCHEMAS (The Java Request/Response DTO equivalents)
# =====================================================================

class UserRegisterRequest(BaseModel):
    """Java Equivalent: UserRegisterRequestDTO. Handles incoming request body validation."""
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    """Java Equivalent: UserResponseDTO. Filters out sensitive fields before returning JSON."""
    id: int
    username: str
    email: str

    # Tells Pydantic to read standard ORM/SQLAlchemy objects smoothly
    class Config:
        from_attributes = True