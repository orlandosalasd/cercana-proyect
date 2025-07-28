from pydantic import BaseModel, Field


class Token(BaseModel):
    """Schema from system token"""

    access_token: str = Field(..., description="Access token user from system")
    token_type: str = Field(..., description="bearer")
