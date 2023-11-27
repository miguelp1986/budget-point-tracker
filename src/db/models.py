"""
Database Models
"""

from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str  # Store hashed and salted password
    email: str
    # Add other user-related fields here

    # Relationships
    accounts: List["Account"] = Relationship(back_populates="user")
    budgets: List["Budget"] = Relationship(back_populates="user")
    loyalty_programs: List["LoyaltyProgram"] = Relationship(back_populates="user")
    transactions: List["Transaction"] = Relationship(back_populates="user")


class Account(SQLModel, table=True):
    account_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    account_type: str  # checking, savings, or credit card
    balance: float

    # Relationships
    user: User = Relationship(back_populates="accounts")
    transactions: List["Transaction"] = Relationship(back_populates="account")


class Budget(SQLModel, table=True):
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
    loyalty_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    program_name: str
    points: int
    last_updated_date: datetime

    # Relationships
    user: User = Relationship(back_populates="loyalty_programs")
