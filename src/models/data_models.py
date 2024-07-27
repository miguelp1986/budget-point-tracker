"""
Data models
"""

from pydantic import BaseModel, EmailStr, StringConstraints
from typing_extensions import Annotated


class UserCreate(BaseModel):
    """User model for creating a new user with a password"""

    username: Annotated[str, StringConstraints(min_length=3, max_length=50)]
    email: EmailStr  # use EmailStr for Pydantic
    password: Annotated[str, StringConstraints(min_length=9, max_length=50)]


class UserResponse(BaseModel):
    """User model for returning user information"""

    user_id: int
    username: Annotated[str, StringConstraints(min_length=3, max_length=50)]
    email: EmailStr  # use EmailStr for Pydantic


class LoginData(BaseModel):
    """User model for login data"""

    username: str
    password: str
