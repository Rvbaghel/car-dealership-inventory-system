from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.entities.user_entity import UserEntity, UserRegisterRequest, UserResponse
from app.security.jwt_handler import SecurityUtils  # 1. Import security helper

class AuthService:
    """Java Equivalent: @Service class handling core authentication business validation rules."""
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, request: UserRegisterRequest) -> UserResponse:
        if self.user_repo.find_by_username(request.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Username already exists"
            )
            
        if self.user_repo.find_by_email(request.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email already exists"
            )

        # 2. Refactored: Encrypt the plain text password securely using Bcrypt
        secure_hashed_password = SecurityUtils.hash_password(request.password)

        new_user = UserEntity(
            username=request.username,
            email=request.email,
            hashed_password=secure_hashed_password  # Store the secure hash string!
        )

        saved_user = self.user_repo.save(new_user)
        return UserResponse.model_validate(saved_user)