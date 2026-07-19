from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # 🟢 Imported cleanly
from sqlalchemy import text 
from app.config import engine, Base, SessionLocal
from app.controllers import auth_controller
from app.entities.user_entity import UserEntity
from app.security.jwt_handler import SecurityUtils
from app.controllers.vehicle_controller import router as vehicle_router
from app.config import settings

def seed_admin_user():
    db = SessionLocal()
    try:
        admin_email = "admin@dealership.com"
        admin = db.query(UserEntity).filter(UserEntity.email == admin_email).first()
        
        if not admin:
            hashed_pass = SecurityUtils.hash_password(settings.ADMIN_SEED_PASSWORD)
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

# 🟢 1. Initialize the FastAPI instance first!
app = FastAPI(
    title="Car Dealership Inventory System",
    description="Java-style Architecture Full-Stack Assessment API",
    version="1.0.0",
    lifespan=lifespan
)

# 🟢 2. Enforce the CORS policy setup right after app definition
origins = [
    "http://localhost:5173",      # Local React/Vite development server
    "http://127.0.0.1:5173",    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # Connects cleanly to our React client
    allow_credentials=True,
    allow_methods=["*"],             
    allow_headers=["*"], 
                
)

# 🟢 3. Mount all domain routing modules smoothly
app.include_router(auth_controller.router)
app.include_router(vehicle_router)

@app.get("/")
def read_root():
    return {"message": "Hello World - Car Dealership Inventory API is Live!"}