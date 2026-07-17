from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import engine, Base
from app.controllers import auth_controller

# Java Equivalent: ApplicationContextInitializer handling schema population safely on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Only creates physical tables if they don't exist yet on normal runtime launch
    Base.metadata.create_all(bind=engine)
    yield  # Hand over control to the active application lifecycle context

app = FastAPI(
    title="Car Dealership Inventory System",
    description="Java-style Architecture Full-Stack Assessment API",
    version="1.0.0",
    lifespan=lifespan
)

# Mount the Authentication Controller Router into the app instance
app.include_router(auth_controller.router)

@app.get("/")
def read_root():
    return {"message": "Hello World - Car Dealership Inventory API is Live!"}