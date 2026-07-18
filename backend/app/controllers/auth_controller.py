from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config import get_db
from app.entities.user_entity import UserRegisterRequest, UserResponse, UserLoginRequest
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication Controller Layer"]
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: UserRegisterRequest, db: Session = Depends(get_db)):
    return AuthService.register_user(request, db)

@router.post("/login", status_code=status.HTTP_200_OK)
def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    return AuthService.authenticate_user(request, db)