import os
from datetime import datetime, timedelta, timezone
import bcrypt  # Direct native library instead of passlib
import jwt
from dotenv import load_dotenv

load_dotenv()

class SecurityUtils:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_temporary_development_key")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    @staticmethod
    def hash_password(password: str) -> str:
        """Uses native bcrypt engine to generate a secure, salt-backed hash string."""
        # Convert clear text string to raw bytes
        password_bytes = password.encode('utf-8')
        # Generate random unique salt signature
        salt = bcrypt.gensalt()
        # Hash and return as a clean decoded text string for storage
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Compares incoming plain text password against stored hash value."""
        try:
            plain_bytes = plain_password.encode('utf-8')
            hashed_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(plain_bytes, hashed_bytes)
        except Exception:
            return False

    @staticmethod
    def is_strong_password(password: str) -> bool:
        if len(password) < 6:
            return False
        import re
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[ !@#$%^&*()_+=\[{\]};:<>|./?,-]", password):
            return False
        return True

    @staticmethod
    def generate_access_token(user_id: int, role: str) -> str:
        now = datetime.now(timezone.utc)
        expire_time = now + timedelta(minutes=SecurityUtils.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        payload = {
            "sub": str(user_id),
            "role": role,
            "iat": int(now.timestamp()),
            "exp": int(expire_time.timestamp())
        }
        
        return jwt.encode(payload, SecurityUtils.SECRET_KEY, algorithm=SecurityUtils.ALGORITHM)