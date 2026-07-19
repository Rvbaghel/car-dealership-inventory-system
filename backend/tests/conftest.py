import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from app.security.jwt_handler import SecurityUtils # Adjust this import if your file is named differently
from app.main import app
from app.config import Base, get_db  # Imported get_db to fix NameError boundary crashes

# 1. Configure our isolated, temporary, in-memory SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# 2. Setup the test engine with StaticPool to keep the memory connection persistent
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# 3. Create our isolated test session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Provides an isolated, clean memory database instance per test run execution."""
    # Build the required clean schema tables inside the memory engine context
    Base.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop tables to guarantee complete isolation boundaries for the next execution pass
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Java Equivalent: MockMvc container utilizing explicit database bean overrides."""
    
    # 4. Create an override helper function that redirects endpoints to the isolated test session
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # 5. Inject the mock session directly into the FastAPI dependency container mapping
    app.dependency_overrides[get_db] = override_get_db
    
    # 6. Override the global database session context factory so the seed function runs against memory
    import app.main as main_module
    original_session_local = main_module.SessionLocal
    main_module.SessionLocal = TestingSessionLocal

    try:
        # Trigger the baseline startup admin seed step inside the active memory context
        main_module.seed_admin_user()
        
        with TestClient(app) as test_client:
            yield test_client
    finally:
        # Restore original production session factories and clear overrides
        main_module.SessionLocal = original_session_local
        app.dependency_overrides.clear()

@pytest.fixture
def admin_client(client):
    """Fixture that returns a test client authenticated as an ADMIN."""
    # Pass arguments directly matching your security layer signature
    token = SecurityUtils.generate_access_token("1", "ADMIN")
    client.headers = {"Authorization": f"Bearer {token}"}
    return client

@pytest.fixture
def user_client(client):
    """Fixture that returns a test client authenticated as a standard USER."""
    # Pass arguments directly matching your security layer signature
    token = SecurityUtils.generate_access_token("2", "USER")
    client.headers = {"Authorization": f"Bearer {token}"}
    return client
    
@pytest.fixture
def test_db_vehicle(db_session):
    """Fixture to create a temporary test vehicle in the DB if you don't have one yet."""
    from app.entities.vehicle_entity import Vehicle
    vehicle = Vehicle(make="Ford", model="Explorer", category="SUV", price=40000, quantity=8)
    db_session.add(vehicle)
    db_session.commit()
    db_session.refresh(vehicle)
    return vehicle        