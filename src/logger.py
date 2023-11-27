"""
Create logger for the application
"""

import logging
from datetime import datetime


def _create_logger(
    name: str = "app", dir: str = "/tmp", level: int = logging.DEBUG
) -> logging.Logger:
    """
    Create logger for the application and save to file.
    Default name is app.
    Default level is DEBUG.
    Default log path is /tmp/app_%Y-%m-%d_%H:%M:%S.log
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a datetime string in YYYY-MM-DD_HH:MM:SS format and append to log path
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d_%H:%M:%S")
    log_path = f"{dir}/{name}_{date_string}.log"

    # Create file handler
    fh = logging.FileHandler(log_path)
    fh.setLevel(level)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # Create formatter and add it to handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def get_logger(name: str = "app") -> logging.Logger:
    """
    Get logger for the application
    """
    # check if logger exists
    if name in logging.Logger.manager.loggerDict:
        return logging.getLogger(name)
    else:
        # create logger
        return _create_logger(name)
