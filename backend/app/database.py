from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
import os
from dotenv import load_dotenv

# Load environment variables from .env file located in the parent directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Get the database URL from environment variable
DATABASE_URL = os.getenv('DATABASE_URL')

# Raise an error if DATABASE_URL is not set
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create the SQLAlchemy engine
engine = create_engine(str(DATABASE_URL), echo=True, connect_args={"check_same_thread": False})

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Create all tables in the database
Base.metadata.create_all(bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
