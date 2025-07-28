from sqlalchemy.orm import Session
from app.services.jwt import create_access_token
from app.db.repositories.user import UserRepository
from app.schemas.token import Token
from app.db.models.user import User
from passlib.context import CryptContext
from app.exceptions import InvalidCredentials, EmailAlreadyExists
from app.schemas.user import UserCreate, UserRead
from app.schemas.auth import Login


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """verify plain password with hashed password.

    Args:
        plain_password (str): password to validate.
        hashed_password (str): hashed passwod to compare with plain password.

    Returns:
        bool: if the passwords validation is correct or not.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """hash the str password.

    Args:
        password (str): password to hash.

    Returns:
        str: password with hash.
    """
    return pwd_context.hash(password)


def authenticate_user(db: Session, data: Login) -> User:
    """authenticate user from email.

    Args:
        db (Session): database session.
        email (str): email from user.
        password (str): password from user.

    Returns:
        User: User instance.
    """
    user_repository = UserRepository(db)
    user = user_repository.get_user_by_email(data.email)
    if not user or not verify_password(data.password, user.password):
        return None
    return user


def login_user(db: Session, data: Login) -> Token:
    """login service from users in system

    Args:
        db (Session): database session.
        email (str): email from user.
        password (str): password from user.

    Raises:
        HTTPException: invalid credentials from user

    Returns:
        Token: token generated.
    """
    user = authenticate_user(db, data)
    if not user:
        raise InvalidCredentials()

    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    return Token(access_token=access_token, token_type="bearer")


def register_user(db: Session, data: UserCreate) -> UserRead:
    """Register user service.

    Args:
        db (Session): Database session.
        data (UserCreate): UserCreate data.

    Returns:
        UserRead: _description_
    """
    user_repository = UserRepository(db)
    user = user_repository.get_user_by_email(data.email)
    if user:
        raise EmailAlreadyExists(data.email)
    data.password = get_password_hash(data.password)
    user = user_repository.create(data)
    return UserRead.model_validate(user, from_attributes=True)
