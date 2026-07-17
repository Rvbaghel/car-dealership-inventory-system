from fastapi import FastAPI
from app.config import engine, Base
from app.controllers import auth_controller  # 1. Import your auth controller module

# Automatically creates the tables inside local_dealership.db if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Car Dealership Inventory System",
    description="Java-style Architecture Full-Stack Assessment API",
    version="1.0.0"
)

# 2. Mount the Authentication Controller Router into the app instance
app.include_router(auth_controller.router)

@app.get("/")
def read_root():
    return {"message": "Hello World - Car Dealership Inventory API is Live!"}