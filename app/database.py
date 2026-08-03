from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# This creates a file named "resume_screener.db" in your root folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./resume_screener.db"

# connect_args={"check_same_thread": False} is required only for SQLite in FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the database session in our API routes later
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()