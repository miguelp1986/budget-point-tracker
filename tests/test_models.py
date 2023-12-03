"""
Tests for DB models
"""

import os
from datetime import datetime

import pytest
from sqlmodel import Session, SQLModel, create_engine, select

from src.db.models import Account, Budget, User

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
    test_user = _create_add_commit_test_user(
        session=session,
        username="testuser",
        password="testpassword",
        email="test@example.com",
    )
    session.refresh(test_user)

    # Check that the user was created
    assert test_user.user_id is not None


def test_read_user(session):
    """
    Test that a user can be read.
    """
    # Create and commit a new user
    _create_add_commit_test_user(
        session=session,
        username="testuser2",
        password="testpassword2",
        email="test2@example.com",
    )

    # Read the user back from the database
    result = session.exec(select(User).where(User.username == "testuser2"))
    user = result.first()

    # Assert that a user was retrieved
    assert user is not None, "No user found in the database"
    # Assert that the retrieved user matches the created user
    if user:
        # Assert that the retrieved user matches the created user
        assert user.username == "testuser2", "Username does not match"
        assert user.email == "test2@example.com", "Email does not match"


def _create_add_commit_test_user(
    session: Session, username: str, password: str, email: str
) -> User:
    """
    Create a test user.
    """
    test_user = User(username=username, password=password, email=email)
    session.add(test_user)
    session.commit()
    return test_user


def test_create_account(session):
    """
    Test creating an account.
    """
    # Create a user
    test_user = _create_add_commit_test_user(
        session=session,
        username="user_for_account",
        password="password",
        email="user@account.com",
    )
    session.refresh(test_user)

    # Create an account
    test_account = _create_add_commit_test_account(
        session=session,
        user_id=test_user.user_id,
        account_type="checking",
        balance=1000.0,
    )
    session.refresh(test_account)
    # Check that the account was created
    assert test_account.account_id is not None


def test_read_account(session):
    """
    Test reading an account from the database.
    """
    # Create a user and an account
    test_user = _create_add_commit_test_user(
        session=session,
        username="user_for_account",
        password="password",
        email="email.com",
    )
    test_account = _create_add_commit_test_account(
        session=session,
        user_id=test_user.user_id,
        account_type="checking",
        balance=1000.0,
    )

    # Read the account back from the database
    result = session.exec(
        select(Account).where(Account.account_id == test_account.account_id)
    )
    account = result.first()

    # Assert that an account was retrieved
    assert account is not None, "No account found in the database"
    # Assert that the retrieved account matches the created account
    if account:
        assert account.account_type == "checking", "Account type does not match"
        assert account.balance == 1000.0, "Account balance does not match"


def _create_add_commit_test_account(
    session: Session, user_id: int, account_type: str, balance: float
) -> Account:
    """
    Create a test account.
    """
    test_account = Account(user_id=user_id, account_type=account_type, balance=balance)
    session.add(test_account)
    session.commit()
    return test_account


def test_create_budget(session):
    """
    Test creating a budget.
    """
    # Create a user
    test_user = _create_add_commit_test_user(
        session=session,
        username="user_for_budget",
        password="password",
        email="email.com",
    )

    session.refresh(test_user)

    # Create a budget
    test_budget = _create_add_commit_test_budget(
        session=session,
        user_id=test_user.user_id,
        name="test budget",
        amount=1000.0,
        start_date=datetime(2021, 1, 1),
        end_date=datetime(2021, 1, 31),
    )

    session.refresh(test_budget)
    # Check that the budget was created
    assert test_budget.budget_id is not None


def test_read_budget(session):
    """
    Test reading a budget from the database.
    """
    # Create a user
    test_user = _create_add_commit_test_user(
        session=session,
        username="user_for_budget",
        password="password",
        email="email.com",
    )

    session.refresh(test_user)

    # Create a budget
    test_budget = _create_add_commit_test_budget(
        session=session,
        user_id=test_user.user_id,
        name="test budget",
        amount=1000.0,
        start_date=datetime(2021, 1, 1),
        end_date=datetime(2021, 1, 31),
    )

    session.refresh(test_budget)

    # Read the budget back from the database
    result = session.exec(
        select(Budget).where(Budget.budget_id == test_budget.budget_id)
    )
    budget = result.first()

    # Assert that a budget was retrieved
    assert budget is not None, "No budget found in the database"
    # Assert that the retrieved budget matches the created budget
    if budget:
        assert budget.name == "test budget", "Budget name does not match"
        assert budget.amount == 1000.0, "Budget amount does not match"


def _create_add_commit_test_budget(
    session: Session,
    user_id: int,
    name: str,
    amount: float,
    start_date: datetime,
    end_date: datetime,
) -> Budget:
    """
    Create a test budget.
    """
    test_budget = Budget(
        user_id=user_id,
        name=name,
        amount=amount,
        start_date=start_date,
        end_date=end_date,
    )
    session.add(test_budget)
    session.commit()
    return test_budget
