import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.config import Base, get_db  # Import our schema base metadata and real dependency hook

# 1. Configure our isolated, temporary, in-memory SQLite URL
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# 2. Setup the test engine with StaticPool to keep the memory connection persistent
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# 3. Create our session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Provides an isolated, clean memory database instance per test run execution."""
    # Build schema maps directly inside our temporary memory container
    Base.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop the structures entirely when done so no dirty records cross over
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Java Equivalent: MockMvc container utilizing explicit database bean overrides."""
    
    # 4. Create an override helper function that catches endpoints requesting get_db
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # 5. Inject the mock session directly into the FastAPI application bean mapping
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
        
    # 6. Clear overrides after the test finishes to preserve production behavior
    app.dependency_overrides.clear()