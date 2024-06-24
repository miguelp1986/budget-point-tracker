from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, SQLModel, select

from src.db.database import engine, get_db
from src.db.models import User
from src.utils.config import load_env
from src.utils.logger import get_logger

# Load environment variables
load_env()  # do we need this here?

# Get or create logger
logger = get_logger()

app = FastAPI()


@app.on_event("startup")
def on_startup():
    """
    TODO: Initial development and testing only
    Use Alembic for migrations in production.

    Create the database tables on startup
    """
    SQLModel.metadata.create_all(engine)


@app.post("/api/v1/users/register")
def register_user(user: User, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password before saving
    user.hash_password(user.password)

    # Save the new user to the database
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"user_id": user.user_id, "username": user.username, "email": user.email}


@app.get("/")
def read_root():
    """."""
    logger.info("Mic check")
    return {"Mic check": 12}
