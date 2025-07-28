from pydantic import BaseModel, Field


class Login(BaseModel):
    """Schema for login."""

    email: str = Field(
        ..., description="Email from user", example="orlando@example.com"
    )

    password: str = Field(
        ..., description="Password for the user's account", example="Password123!"
    )
