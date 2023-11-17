import logging


# Create a logger
def setup_logger(log_level=logging.INFO):
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create a file handler and set the level to DEBUG
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(log_level)

    # Create a formatter and add it to the file handler
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger
