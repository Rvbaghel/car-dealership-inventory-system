from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config import get_db
from app.entities.user_entity import UserRegisterRequest, UserResponse, UserLoginRequest
from app.services.auth_service import AuthService
from fastapi import Depends, Header
from app.security.jwt_handler import SecurityUtils

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

@router.get("/profile")
def get_user_profile(authorization: str = Header(None)):
    """A protected endpoint to verify our JWT generation and validation live."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header structural format")
    
    # Extract the token string out from behind the "Bearer " scheme
    token = authorization.split(" ")[1]
    
    # Run verification check
    payload = SecurityUtils.verify_access_token(token)
    
    return {
        "status": "Authenticated",
        "message": "Token verification successful!",
        "user_id": payload.get("sub"),
        "role": payload.get("role")
    }