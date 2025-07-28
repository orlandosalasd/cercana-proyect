from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    """Base schema for a user."""

    full_name: str = Field(
        ..., description="Full name of the user", example="Orlando Salas"
    )
    email: str = Field(
        ..., description="Email from user", example="orlando@example.com"
    )


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(
        ..., description="Password for the user's account", example="Password123!"
    )


class UserUpdate(UserBase):
    """Base schema for update user."""

    full_name: Optional[str] = Field(
        ..., description="Full name of the user", example="Orlando Salas"
    )
    email: Optional[str] = Field(
        ..., description="Email from user", example="orlando@example.com"
    )


class UserRead(UserBase):
    """Schema for returning user data (excluding sensitive fields like password)."""

    id: int = Field(..., description="Unique identifier of the user", example=1)

    model_config = ConfigDict(from_attributes=True)
