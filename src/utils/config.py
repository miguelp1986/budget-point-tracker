"""
Configuration-related utilities
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

    # Get the .env file based on the environment. Default to .env.dev
    env_file = {"prod": ".env.prod", "test": ".env.test", "dev": ".env.dev"}.get(
        env_type, ".env.dev"
    )

    # Build the path to the .env file
    env_path = ROOT_DIR / env_file
    logger.debug(f"Loading environment variables from {env_path}")

    # Load the .env file
    load_dotenv(dotenv_path=env_path)


def get_database_url():
    """Get the database URL based on the environment."""
    url = os.getenv("DATABASE_URL")
    if not url:
        raise OSError("DATABASE_URL is not set in environment")

    return url


def get_pytest_database_url():
    """Get the test database URL."""
    pytest_db_url = os.getenv("PYTEST_DATABASE_URL")
    if not pytest_db_url:
        raise OSError("PYTEST_DATABASE_URL is not set in environment")

    return pytest_db_url
