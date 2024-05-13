"""
Configuration related utilities
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from src.utils.logger import get_logger

ROOT_DIR = Path(__file__).parent.parent.parent.absolute()
SOURCE_DIR = Path(__file__).parent.parent.absolute()

# Get or create logger
logger = get_logger()


def load_env():
    """Load environment variables from .env file"""
    env_type = os.getenv("ENV_TYPE", "dev")  # Default to 'dev' if not set

    # Map the environment type to the .env file name
    env_file = {"prod": ".env.prod", "test": ".env.test", "dev": ".env.dev"}.get(
        env_type, ".env.dev"
    )  # Default to .env.dev if unrecognized

    # Build the path to the .env file
    env_path = ROOT_DIR / env_file
    logger.debug(f"Loading environment variables from {env_path}")

    # Load the .env file
    load_dotenv(dotenv_path=env_path)


def get_database_url():
    """Get the database URL based on the environment."""
    env = os.getenv("ENV")

    if env == "testing":
        url = os.getenv("TEST_DATABASE_URL")
        if not url:
            raise OSError("TEST_DATABASE_URL is not set in testing environment")
        return url

    elif env == "production":
        url = os.getenv("PROD_DATABASE_URL")
        if not url:
            raise OSError("PROD_DATABASE_URL is not set in production environment")
        return url

    elif env == "development":
        url = os.getenv("DEV_DATABASE_URL")
        if not url:
            raise OSError("DEV_DATABASE_URL is not set in development environment")
        return url

    else:
        raise OSError("Unknown environment or ENV variable not set")


def get_pytest_database_url():
    """Get the test database URL."""
    pytest_db_url = os.getenv("PYTEST_DATABASE_URL")
    if not pytest_db_url:
        raise OSError("PYTEST_DATABASE_URL is not set")

    return pytest_db_url
