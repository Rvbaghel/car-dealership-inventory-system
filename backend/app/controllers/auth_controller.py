from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config import get_db
from app.entities.user_entity import UserRegisterRequest, UserResponse
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

# Java Equivalent: @RequestMapping("/api/auth")
router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Java Equivalent: @PostMapping("/register") with HttpStatus.CREATED (201)
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: UserRegisterRequest, db: Session = Depends(get_db)):
    """
    Java Equivalent: Handles Dependency Injection of the DB session, 
    instantiates the layered components, and returns the response body.
    """
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    return auth_service.register_user(request)