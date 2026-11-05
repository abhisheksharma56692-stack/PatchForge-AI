"""SQLAlchemy engine, session factory, and database initialization."""
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from patchforge.config import settings
from patchforge.db.base import Base

# Engine configuration
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a managed database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Creates all relational database tables and seeds initial data if empty."""
    Base.metadata.create_all(bind=engine)
    
    # Import and run seed inside a session
    from patchforge.db.seed import seed_initial_data
    db = SessionLocal()
    try:
        seed_initial_data(db)
    finally:
        db.close()

