from fastapi import FastAPI

from src.utils.logger import get_logger

app = FastAPI()

# Create a logger
logger = get_logger()


@app.get("/")
def read_root():
    """."""
    logger.info("Mic check")
    return {"Mic check": 12}
