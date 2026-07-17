from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.entities.user_entity import UserEntity, UserRegisterRequest, UserResponse

class AuthService:
    """Java Equivalent: @Service class handling core authentication business validation rules."""
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, request: UserRegisterRequest) -> UserResponse:
        # 1. Core Validation Rules: Ensure username and emails are completely unique
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

        # 2. Map incoming Request DTO to Database Entity Model
        new_user = UserEntity(
            username=request.username,
            email=request.email,
            hashed_password=request.password  # Raw password temporarily (Will secure in refactor!)
        )

        # 3. Persist record down to the database layer
        saved_user = self.user_repo.save(new_user)
        
        # 4. Map the saved Entity back to a secure Response DTO structure (Filters out password)
        return UserResponse.model_validate(saved_user)