from fastapi import APIRouter, Depends, HTTPException
from app.services.auth import login_user, register_user
from app.schemas.user import UserCreate, UserRead
from app.schemas.auth import Login
from app.schemas.token import Token
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.exceptions import InvalidCredentials, EmailAlreadyExists

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(data: Login, db: Session = Depends(get_db)) -> Token:
    """Login in system with credentials

    Args:
        data (Login): Login Schema
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If credentials was invalid

    Returns:
        Token: User JWT
    """
    try:
        user_token = login_user(db, data)
    except InvalidCredentials as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user_token


@router.post("/register", response_model=UserRead)
def register(data: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    """Register new user.

    Args:
        data (UserCreate): Data from new user.
        db (Session, optional): Database Session. Defaults to Depends(get_db).

    Returns:
        UserRead: User read data.
    """
    try:
        user = register_user(db, data)
    except EmailAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user
