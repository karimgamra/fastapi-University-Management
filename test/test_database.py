from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.schemas.user import User
# Use SQLite in-memory database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # or use a test.db file

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)


def override_get_current_user():
    return User(id=1, name="karim", email="karim@gmail.com", role="admin")


# Dependency override for tests
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
