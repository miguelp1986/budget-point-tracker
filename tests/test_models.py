"""
Tests for DB models
"""

import os

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import User

# Use test database
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
engine = create_async_engine(TEST_DATABASE_URL, echo=True)

# Sessionmaker for async session
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(name="session", scope="function")
async def session_fixture():
    """
    Create a clean database on each test case
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_user(session):
    """
    Test that a user can be created
    """
    async with session.begin():
        user = User(
            username="testuser", password="testpassword", email="test@example.com"
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        assert user.id is not None


@pytest.mark.asyncio
async def test_read_user(session):
    """
    Test that a user can be read
    """
    async with session.begin():
        result = await session.execute(
            select(User).where(User.username == "testuser")
        ).first()
        user = result.scalars().first()
        assert user.username == "testuser"
        assert user.email == "test@example.com"
