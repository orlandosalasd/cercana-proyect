from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    """
    ORM model represent a user in system.

    Attributes:
        id (int): Unique identifier.
        full_name (str): The user's full name.
        email (str): The user's email address.
        hashed_password (str): The user's password, stored in a hashed format.
        task_lists (List[TaskList]): List of task lists associated with the user.
        tasks (List[Task]): List of tasks.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    task_lists = relationship("TaskList", back_populates="user")
    tasks = relationship("Task", back_populates="in_charge")
