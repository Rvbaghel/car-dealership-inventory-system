from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text  # Standard SQL wrapper to target internal tables
from app.config import engine, Base, SessionLocal
from app.controllers import auth_controller
from app.entities.user_entity import UserEntity
from app.security.jwt_handler import SecurityUtils

def seed_admin_user():
    db = SessionLocal()
    try:
        admin_email = "admin@dealership.com"
        admin = db.query(UserEntity).filter(UserEntity.email == admin_email).first()
        
        if not admin:
            hashed_pass = SecurityUtils.hash_password("SuperSecureAdminPassword123!")
            admin_user = UserEntity(
                username="admin",
                email=admin_email,
                hashed_password=hashed_pass,
                role="ADMIN"
            )
            db.add(admin_user)
            db.commit()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    
   # Generates all missing tables and columns cleanly on startup
    Base.metadata.create_all(bind=engine)
    
    # Executes database seeding routines
    seed_admin_user()
    yield

app = FastAPI(
    title="Car Dealership Inventory System",
    description="Java-style Architecture Full-Stack Assessment API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth_controller.router)

@app.get("/")
def read_root():
    return {"message": "Hello World - Car Dealership Inventory API is Live!"}