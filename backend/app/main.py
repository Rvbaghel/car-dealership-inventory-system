from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import engine, Base, SessionLocal
from app.controllers import auth_controller
from app.entities.user_entity import UserEntity
from app.security.jwt_handler import SecurityUtils

# Java Equivalent: DatabaseInitializer seeding critical production beans on system container creation
def seed_admin_user():
    db = SessionLocal()
    try:
        # Check if the core admin identity profile exists in storage layers
        admin_email = "admin@dealership.com"
        admin = db.query(UserEntity).filter(UserEntity.email == admin_email).first()
        
        if not admin:
            hashed_pass = SecurityUtils.hash_password("SuperSecureAdminPassword123!")
            admin_user = UserEntity(
                username="admin",
                email=admin_email,
                hashed_password=hashed_pass,
                role="ADMIN"  # Elevate permissions explicitly to Admin role status
            )
            db.add(admin_user)
            db.commit()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure tables are built
    Base.metadata.create_all(bind=engine)
    # Execute database migration/seeding profiles
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