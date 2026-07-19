from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # ... your other config settings ...
    ADMIN_SEED_PASSWORD: str = os.getenv("ADMIN_SEED_PASSWORD", "FallbackSecurePasswordIfEnvMissing123!")

settings = Settings()

# 1. Database file path
DATABASE_URL = "sqlite:///./local_dealership.db"

# 2. Setup the engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# 3. Create SessionLocal factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the declarative Base class
Base = declarative_base()

def get_db():
    """Provides a transactional database session context per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()