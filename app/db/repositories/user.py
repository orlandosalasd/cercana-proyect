from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    """User class repository."""

    def __init__(self, db: Session) -> None:
        """Constructor class method.

        Args:
            db (Session): Session from database.
        """
        self.db = db

    def create(self, data: UserCreate) -> User:
        """User repository function to create.

        Args:
            data (UserCreate): Schema to create user.

        Returns:
            User: User instance.
        """
        user = User(**data.model_dump())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: int, data: UserUpdate) -> User | None:
        """User repository function to update.

        Args:
            user_id (int): User id.
            data (UserUpdate): Schema to update user.

        Returns:
            User | None: User instance if user exits or None if not.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        for key, value in data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        """User repository function to delete.

        Args:
            user_id (int): User id.

        Returns:
            bool: If user was deleted
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        self.db.delete(user)
        self.db.commit()
        return True

    def get_user_by_id(self, user_id: int) -> User | None:
        """User repository function to get user by id.

        Args:
            user_id (int): User id.

        Returns:
            User | None: User instance if user exits or None if not.
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, user_email: str) -> User | None:
        """User repository function to get user by email.

        Args:
            user_email (str): User email.

        Returns:
            User | None: User instance if user exits or None if not.
        """
        return self.db.query(User).filter(User.email == user_email).first()
