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


class Config:
    """
    Configuration class to manage environment variables
    """

    def __init__(self):
        self.load_env()

    def load_env(self):
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

    @staticmethod
    def get_env_var(key: str, default: str = None):
        value = os.getenv(key, default)
        if value is None:
            raise ValueError(
                f"No {key} set for the application and no default value provided"
            )
        return value

    @property
    def fastapi_host(self):
        return self.get_env_var("FASTAPI_HOST", "0.0.0.0")

    @property
    def fastapi_port(self):
        return int(self.get_env_var("FASTAPI_PORT", "8000"))

    @property
    def database_url(self):
        return self.get_env_var("DATABASE_URL")

    @property
    def database_host(self):
        return self.get_env_var("DATABASE_HOST", "localhost")

    @property
    def database_user(self):
        return self.get_env_var("DATABASE_USER")

    @property
    def database_port(self):
        return int(self.get_env_var("DATABASE_PORT", "5432"))

    @property
    def database_password(self):
        return self.get_env_var("DATABASE_PASSWORD")

    @property
    def database_name(self):
        return self.get_env_var("DATABASE_NAME")

    @property
    def pytest_database_url(self):
        return self.get_env_var("PYTEST_DATABASE_URL")

    @property
    def pytest_database_host(self):
        return self.get_env_var("PYTEST_DATABASE_HOST", "localhost")

    @property
    def pytest_database_user(self):
        return self.get_env_var("PYTEST_DATABASE_USER")

    @property
    def pytest_database_port(self):
        return int(self.get_env_var("PYTEST_DATABASE_PORT", "5432"))

    @property
    def pytest_database_password(self):
        return self.get_env_var("PYTEST_DATABASE_PASSWORD")

    @property
    def pytest_database_name(self):
        return self.get_env_var("PYTEST_DATABASE_NAME")

    @property
    def docker_image(self):
        return self.get_env_var("DOCKER_IMAGE")

    @property
    def docker_tag(self):
        return self.get_env_var("DOCKER_TAG", "latest")

    @property
    def secret_key(self):
        return self.get_env_var("SECRET_KEY")

    @property
    def algorithm(self):
        return self.get_env_var("ALGORITHM", "HS256")

    @property
    def access_token_expire_minutes(self):
        return int(self.get_env_var("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
