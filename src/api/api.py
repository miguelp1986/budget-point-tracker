from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, SQLModel, select

from src.db.database import engine, get_db
from src.db.models import User, UserCreate, UserResponse
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
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = User.model_validate(user)  # validate the user data
    new_user.hash_password(user.password)  # hash user password

    # Save the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # return the new user
    return UserResponse(
        user_id=new_user.user_id, username=new_user.username, email=new_user.email
    )


@app.get("/")
def read_root():
    """."""
    logger.info("Mic check")
    return {"Mic check": 12}
