"""
Configuration related utilities
"""

import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.absolute()


def get_database_url():
    """Get the database URL based on the environment."""
    if os.getenv("ENV") == "testing":
        return os.getenv("TEST_DATABASE_URL")

    elif os.getenv("ENV") == "production":
        return os.getenv("PROD_DATABASE_URL")

    else:
        return os.getenv("DEV_DATABASE_URL")
