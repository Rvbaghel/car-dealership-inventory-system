from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # ... your other config settings ...
    ADMIN_SEED_PASSWORD: str = os.getenv("ADMIN_SEED_PASSWORD", "FallbackSecurePasswordIfEnvMissing123!")

settings = Settings()

DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Add an explicit check for SQLite connect_args
# SQLite needs `check_same_thread: False`, but PostgreSQL will CRASH if you pass it!
if DATABASE_URL and DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency for your routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()