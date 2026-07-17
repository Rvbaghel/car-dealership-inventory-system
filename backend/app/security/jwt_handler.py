import bcrypt

class SecurityUtils:
    """Java Equivalent: Crypto security encoder service component using native Bcrypt."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes plain text password using strong Bcrypt salting."""
        # Convert text string to UTF-8 bytes, generate a fresh salt, and hash it
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(password_bytes, salt)
        # Decode bytes back to a standard string format to store nicely in SQLite
        return hashed_bytes.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifies if a raw password matches the database hash signature."""
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)