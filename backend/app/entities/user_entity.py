from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from app.config import Base
from app.security.jwt_handler import SecurityUtils

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
# 2. DTO SCHEMAS
# =====================================================================
class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        """Delegates validation to centralized security rule utility."""
        if not SecurityUtils.is_strong_password(value):
            raise ValueError(
                "Password must contain at least one uppercase letter, "
                "one lowercase letter, one numeric digit, and one special character."
            )
        return value

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)