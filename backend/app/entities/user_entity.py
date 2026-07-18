import re
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
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
# 2. DTO SCHEMAS (With Strict Pattern Validations)
# =====================================================================
class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr  # Automatically enforces RFC compliant email verification
    password: str = Field(..., min_length=6)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        """Enforces uppercase, lowercase, special symbols, and numeric characters."""
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one numerical digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")
        return value

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)