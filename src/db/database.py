"""
Contains the database connection and the session maker.
"""

from sqlmodel import Session, create_engine

from src.utils.config import get_database_url

# Using SQLite for now. Change to PostgreSQL in production.
DATABASE_URL = get_database_url()
engine = create_engine(
    DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)


def get_db():
    """Get a database connection."""
    with Session(engine) as session:
        yield session
