from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.db.models.user import User
from app.db.repositories.user import UserRepository
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """create access token with from data.

    Args:
        data (dict): jwt data dict information.
        expires_delta (Optional[timedelta], optional): time to token expiration.
        Defaults to None.

    Returns:
        str: access token.
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    """decode token from request and validate.

    Args:
        token (str): token from request.

    Returns:
        dict: dcit from token with token data.
    """
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """get current user in token.

    Args:
        db (Session): Database session
        token (str, optional): Token from HTTP request.
        Defaults to Depends(oauth2_scheme).

    Raises:
        HTTPException: If token was invalid and not have sub.

    Returns:
        User: User instance
    """
    try:
        payload = decode_token(token)
        user_email = payload.get("email", None)
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_repository = UserRepository(db)
        return user_repository.get_user_by_email(user_email)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
