from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///toolshare.db"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    """Yield a database session for use in services/CLI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    import toolshare.models  
    Base.metadata.create_all(bind=engine)

