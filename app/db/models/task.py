from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SqlEnum
from app.core.enums.general_enums import PriorityEnum, TaskStatusEnum
from app.db.base import Base


class Task(Base):
    """
    ORM model representing a task.

    Attributes:
        id (int): Unique identifier for the task.
        user_id (int): Foreign key referencing the user assigned to this task.
        tasks_lists_id (int): Foreign key referencing the associated task list.
        description (str): Description or details of the task.
        complete (bool): Indicates whether the task is completed.
        priority (str): Priority level of the task.
        in_charge (User): The user responsible for completing the task.
        task_list (TaskList): The task list to which this task belongs.
    """

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    task_list_id = Column(Integer, ForeignKey("task_lists.id"))
    description = Column(String)
    status = Column(
        SqlEnum(TaskStatusEnum, name="task_status_enum"),
        nullable=False,
        default=TaskStatusEnum.PENDING,
    )
    priority = Column(
        SqlEnum(PriorityEnum, name="priority_enum"),
        nullable=False,
        default=PriorityEnum.LOW,
    )

    in_charge = relationship("User", back_populates="tasks")
    task_list = relationship("TaskList", back_populates="tasks")


class TaskList(Base):
    """
    ORM model representing a list of tasks.

    Attributes:
        id (int): Unique identifier for the task list.
        name (str): Name of the task list.
        user_id (int): Foreign key referencing the user who owns this task list.
        user (User): The user who owns this task list.
        tasks (List[Task]): List of tasks associated with this task list.
    """

    __tablename__ = "task_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="task_lists")
    tasks = relationship("Task", back_populates="task_list")
