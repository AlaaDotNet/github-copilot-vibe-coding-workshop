"""
Database configuration and session management.
"""
from typing import Annotated, Generator

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine


# Database configuration
DATABASE_URL = "sqlite:///sns_api.db"

# Create engine with SQLite-specific configuration
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries for debugging
    connect_args={"check_same_thread": False}  # Allow SQLite to be used with FastAPI
)


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session dependency."""
    with Session(engine) as session:
        yield session


# Session dependency type
SessionDep = Annotated[Session, Depends(get_session)]
