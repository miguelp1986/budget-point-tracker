"""
Tests for DB models
"""

from datetime import datetime

import pytest
from sqlmodel import Session, SQLModel, create_engine, select

from src.db.models import Account, Budget, LoyaltyProgram, Transaction, User
from src.utils.config import get_pytest_database_url, load_env

# Load environment variables
load_env()

# Use test database
PYTEST_DATABASE_URL = get_pytest_database_url()
engine = create_engine(PYTEST_DATABASE_URL, echo=True)


@pytest.fixture(name="session", scope="function")
def session_fixture():
    """
    Create a database session for testing
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


def test_create_transaction(session):
    """
    Test creating a transaction.
    """
    # Create a user
    test_user = _create_add_commit_test_user(
        session=session,
        username="user_for_transaction",
        password="password",
        email="email.com",
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

    # Create a transaction
    test_transaction = _create_add_commit_test_transaction(
        session=session,
        user_id=test_user.user_id,
        account_id=test_account.account_id,
        budget_id=test_budget.budget_id,
        date=datetime(2021, 1, 1),
        amount=100.0,
        description="test transaction",
    )

    session.refresh(test_transaction)
    # Check that the transaction was created
    assert test_transaction.transaction_id is not None


def test_read_transaction(session):
    """
    Test reading a transaction from the database.
    """
    # Create a user
    test_user = _create_add_commit_test_user(
        session=session,
        username="user_for_transaction",
        password="password",
        email="email.com",
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

    # Create a transaction
    test_transaction = _create_add_commit_test_transaction(
        session=session,
        user_id=test_user.user_id,
        account_id=test_account.account_id,
        budget_id=test_budget.budget_id,
        date=datetime(2021, 1, 1),
        amount=100.0,
        description="test transaction",
    )

    session.refresh(test_transaction)

    # Read the transaction back from the database
    result = session.exec(
        select(Transaction).where(
            Transaction.transaction_id == test_transaction.transaction_id
        )
    )
    transaction = result.first()

    # Assert that a transaction was retrieved
    assert transaction is not None, "No transaction found in the database"
    # Assert that the retrieved transaction matches the created transaction
    if transaction:
        assert transaction.date == datetime(
            2021, 1, 1
        ), "Transaction date does not match"
        assert transaction.amount == 100.0, "Transaction amount does not match"
        assert (
            transaction.description == "test transaction"
        ), "Transaction description does not match"


def _create_add_commit_test_transaction(
    session: Session,
    user_id: int,
    account_id: int,
    budget_id: int,
    date: datetime,
    amount: float,
    description: str,
) -> Budget:
    """
    Create a test transaction.
    """
    test_transaction = Transaction(
        user_id=user_id,
        account_id=account_id,
        budget_id=budget_id,
        date=date,
        amount=amount,
        description=description,
    )
    session.add(test_transaction)
    session.commit()
    return test_transaction


def test_create_loyalty_program(session):
    """
    Test creating a loyalty program.
    """
    # Create a user
    test_user = _create_add_commit_test_user(
        session=session,
        username="user_for_loyalty_program",
        password="password",
        email="email.com",
    )

    session.refresh(test_user)

    # Create a loyalty program
    test_loyalty_program = _create_add_commit_test_loyalty_program(
        session=session,
        user_id=test_user.user_id,
        program_name="test loyalty program",
        points=1000,
        last_updated_date=datetime(2021, 1, 1),
    )

    session.refresh(test_loyalty_program)
    # Check that the loyalty program was created
    assert test_loyalty_program.loyalty_id is not None


def test_read_loyalty_program(session):
    """
    Test reading a loyalty program from the database.
    """
    # Create a user
    test_user = _create_add_commit_test_user(
        session=session,
        username="user_for_loyalty_program",
        password="password",
        email="email.com",
    )

    session.refresh(test_user)

    # Create a loyalty program
    test_loyalty_program = _create_add_commit_test_loyalty_program(
        session=session,
        user_id=test_user.user_id,
        program_name="test loyalty program",
        points=1000,
        last_updated_date=datetime(2021, 1, 1),
    )

    session.refresh(test_loyalty_program)

    # Read the loyalty program back from the database
    result = session.exec(
        select(LoyaltyProgram).where(
            LoyaltyProgram.loyalty_id == test_loyalty_program.loyalty_id
        )
    )
    loyalty_program = result.first()

    # Assert that a loyalty program was retrieved
    assert loyalty_program is not None, "No loyalty program found in the database"
    # Assert that the retrieved loyalty program matches the created loyalty program
    if loyalty_program:
        assert (
            loyalty_program.program_name == "test loyalty program"
        ), "Loyalty program name does not match"
        assert loyalty_program.points == 1000, "Loyalty program points do not match"
        assert loyalty_program.last_updated_date == datetime(
            2021, 1, 1
        ), "Loyalty program last updated date does not match"


def _create_add_commit_test_loyalty_program(
    session: Session,
    user_id: int,
    program_name: str,
    points: int,
    last_updated_date: datetime,
) -> Budget:
    """
    Create a test loyalty program.
    """
    test_loyalty_program = LoyaltyProgram(
        user_id=user_id,
        program_name=program_name,
        points=points,
        last_updated_date=last_updated_date,
    )
    session.add(test_loyalty_program)
    session.commit()
    return test_loyalty_program
