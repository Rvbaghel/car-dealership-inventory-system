from sqlalchemy.orm import Session
from app.entities.user_entity import UserEntity

class UserRepository:
    """Java Equivalent: UserRepository class handling direct DB interaction via EntityManager."""
    
    def __init__(self, db: Session):
        self.db = db

    def find_by_username(self, username: str) -> UserEntity:
        # Like: return entityManager.createQuery("SELECT u FROM User u WHERE u.username = :username").getSingleResult();
        return self.db.query(UserEntity).filter(UserEntity.username == username).first()

    def find_by_email(self, email: str) -> UserEntity:
        return self.db.query(UserEntity).filter(UserEntity.email == email).first()

    def save(self, user: UserEntity) -> UserEntity:
        # Like: entityManager.persist(user);
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user) # Reloads id and attributes from the database file
        return user