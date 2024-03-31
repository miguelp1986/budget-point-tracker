"""
Database Models
"""

from datetime import datetime
from typing import List, Optional

from passlib.context import CryptContext
from sqlmodel import Field, Relationship, SQLModel

# Create a password context for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(SQLModel, table=True):
    """User model with fields for user information and relationships to other models."""

    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str  # store hashed and salted password
    email: str

    # Relationships
    accounts: List["Account"] = Relationship(back_populates="user")
    budgets: List["Budget"] = Relationship(back_populates="user")
    loyalty_programs: List["LoyaltyProgram"] = Relationship(back_populates="user")
    transactions: List["Transaction"] = Relationship(back_populates="user")

    def hash_password(self, password: str):
        """Hash and salt the password before storing it in the database."""
        self.password = pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str):
        """Verify the password against the hashed password stored in the database."""
        return pwd_context.verify(plain_password, hashed_password)


class Account(SQLModel, table=True):
    """Account model with fields for account information and relationships to other models."""

    account_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    account_type: str  # checking, savings, or credit card
    balance: float

    # Relationships
    user: User = Relationship(back_populates="accounts")
    transactions: List["Transaction"] = Relationship(back_populates="account")


class Budget(SQLModel, table=True):
    """Budget model with fields for budget information and relationships to other models."""

    budget_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    name: str
    amount: float
    start_date: datetime
    end_date: datetime

    # Relationships
    user: User = Relationship(back_populates="budgets")
    transactions: List["Transaction"] = Relationship(back_populates="budget")


class Transaction(SQLModel, table=True):
    """Transaction model with fields for transaction information and relationships to other models."""

    transaction_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    account_id: int = Field(foreign_key="account.account_id")
    budget_id: Optional[int] = Field(default=None, foreign_key="budget.budget_id")
    date: datetime
    amount: float
    description: str

    # Relationships
    user: User = Relationship(back_populates="transactions")
    account: Account = Relationship(back_populates="transactions")
    budget: Optional[Budget] = Relationship(back_populates="transactions")


class LoyaltyProgram(SQLModel, table=True):
    """Loyalty Program model with fields for loyalty program information and relationships to other models."""

    loyalty_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    program_name: str
    points: int
    last_updated_date: datetime

    # Relationships
    user: User = Relationship(back_populates="loyalty_programs")
