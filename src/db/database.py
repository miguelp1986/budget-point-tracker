"""
Contains the database connection and the session maker.
"""

from sqlmodel import Session, create_engine

# Assuming you're using SQLite for simplicity in this example. Replace the URL with your database connection string.
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)


def get_db():
    """Get a database connection."""
    with Session(engine) as session:
        yield session
