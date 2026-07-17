from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Database file path (Will create a local file named local_dealership.db)
DATABASE_URL = "sqlite:///./local_dealership.db"

# 2. Setup the engine (Like configuring your HikariCP Data Source)
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Needed only for SQLite multi-threading
)

# 3. Create SessionLocal factory (Like configuring a JPA EntityManager)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the declarative Base class (Like Spring Boot's JPA / Hibernate Base Entity class)
Base = declarative_base()

def get_db():
    """
    Java Equivalent: Dependency Injection of the Entity Manager / Transaction Management.
    Provides a database session context that auto-closes once the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()