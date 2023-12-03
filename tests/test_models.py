"""
Tests for DB models
"""

import os

import pytest
from sqlmodel import Session, SQLModel, create_engine, select

from src.db.models import User

# Use test database
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
engine = create_engine(TEST_DATABASE_URL, echo=True)


@pytest.fixture(name="session", scope="function")
def session_fixture():
    """
    Create a clean database for each test case.
    """
    # Create all database tables
    SQLModel.metadata.create_all(engine)

    # Connect to the database
    with Session(engine) as session:
        yield session

    # Drop all database tables
    SQLModel.metadata.drop_all(engine)


def test_create_user(session):
    """
    Test that a user can be created.
    """
    # Create a user
    test_user = User(
        username="testuser", password="testpassword", email="test@example.com"
    )
    session.add(test_user)
    session.commit()
    session.refresh(test_user)

    # Check that the user was created
    assert test_user.user_id is not None


def test_read_user(session):
    """
    Test that a user can be read.
    """
    # Create and commit a new user
    test_user = User(
        username="testuser2", password="testpassword2", email="test2@example.com"
    )
    session.add(test_user)
    session.commit()

    # Read the user back from the database
    result = session.exec(select(User).where(User.username == "testuser2"))
    user = result.first()

    # Assert that a user was retrieved
    assert user is not None, "No user found in the database"

    # Proceed with further assertions only if the user is not None
    if user:
        # Assert that the retrieved user matches the created user
        assert user.username == "testuser2", "Username does not match"
        assert user.email == "test2@example.com", "Email does not match"
