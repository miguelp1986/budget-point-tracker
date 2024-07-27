"""
Shared resources for the project
"""

from pathlib import Path

from src.utils.config import Config
from src.utils.logger import get_logger

CONFIG = Config()
LOGGER = get_logger()
ROOT_DIR = Path(__file__).parent.parent.parent.absolute()
