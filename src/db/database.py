"""
Contains the database connection and the session maker.
"""

from sqlmodel import Session, create_engine

from src.utils.shared import CONFIG

# create database engine
DATABASE_URL = CONFIG.database_url
engine = create_engine(url=DATABASE_URL, echo=True)


def get_db():
    """Get a database connection."""
    with Session(engine) as session:
        yield session
