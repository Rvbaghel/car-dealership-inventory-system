from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.entities.user_entity import UserEntity, UserRegisterRequest, UserLoginRequest
from app.repositories.user_repository import UserRepository
from app.security.jwt_handler import SecurityUtils

class AuthService:
    """Java Equivalent: AuthService handling credential validation, profile registration, and token generation."""

    @staticmethod
    def register_user(request: UserRegisterRequest, db: Session) -> UserEntity:
        user_repo = UserRepository(db)

        if user_repo.find_by_username(request.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
        if user_repo.find_by_email(request.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

        secure_hashed_password = SecurityUtils.hash_password(request.password)

        new_user = UserEntity(
            username=request.username,
            email=request.email,
            hashed_password=secure_hashed_password,
            role="USER"
        )

        return user_repo.save(new_user)

    @staticmethod
    def authenticate_user(request: UserLoginRequest, db: Session) -> dict:
        """Verifies credentials and issues a secure signed JWT access token upon success."""
        user_repo = UserRepository(db)
        user = user_repo.find_by_email(request.email)

        if not user or not SecurityUtils.verify_password(request.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Generate our secure 30-minute JWT token payload
        access_token = SecurityUtils.generate_access_token(user_id=user.id, role=user.role)

        # Return compliance dictionary structure
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": user.role
        }