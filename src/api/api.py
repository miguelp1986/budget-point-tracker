from fastapi import FastAPI
from logger import setup_logger

app = FastAPI()

# Create a logger
logger = setup_logger()


@app.get("/")
def read_root():
    """."""
    logger.info("Mic check")
    return {"Mic check": 12}
