"""
Contains the database connection and the session maker.
"""

from sqlmodel import Session, create_engine

from src.utils.config import get_database_url, load_env

# load environment variables
load_env()

# create the database engine
DATABASE_URL = get_database_url()
engine = create_engine(url=DATABASE_URL, echo=True)


def get_db():
    """Get a database connection."""
    with Session(engine) as session:
        yield session
