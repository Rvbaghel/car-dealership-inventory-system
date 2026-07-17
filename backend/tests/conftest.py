import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

# 1. Import your main application instance (Like importing your @SpringBootApplication class)
from app.main import app

# 2. Configure an isolated, temporary, in-memory SQLite URL
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# 3. Create the Database Engine (Like creating a DataSource bean in Java)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}, # Required for SQLite to run across threads
    poolclass=StaticPool,                       # Keeps the in-memory DB alive in a single connection pool
)

# 4. Create a Session Factory (Like configuring your Hibernate/JPA EntityManagerFactory)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Java Equivalent: A helper method that opens a Hibernate Session/EntityManager,
    injects it into a test, and closes/rolls it back after the test completes.
    """
    session = TestingSessionLocal()
    try:
        yield session # This delivers the DB session to whoever requests it
    finally:
        session.close() # Clean up when the test finishes (Ensures isolation)

@pytest.fixture(scope="function")
def client(db_session):
    """
    Java Equivalent: Configuring a MockMvc instance to perform HTTP requests.
    """
    # Using 'with' acts like a try-with-resources block in Java
    with TestClient(app) as test_client:
        yield test_client