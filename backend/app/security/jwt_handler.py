import re
import bcrypt

class SecurityUtils:
    """Java Equivalent: Crypto security encoder service component using native Bcrypt."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes plain text password using strong Bcrypt salting."""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(password_bytes, salt)
        return hashed_bytes.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifies if a raw password matches the database hash signature."""
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)

    @staticmethod
    def is_strong_password(password: str) -> bool:
        """
        Business Rule Verification:
        Enforces 1 Uppercase, 1 Lowercase, 1 Digit, and 1 Special Character.
        """
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True