from sqlalchemy import create_engine 
from sqlalchemy.orm import declarative_base , sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://karim:123@localhost:5432/mydb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


