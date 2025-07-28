from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.core.enums.general_enums import PriorityEnum, TaskStatusEnum


class TaskBase(BaseModel):
    """Base schema for a task."""

    user_id: int = Field(..., description="User id in charge", example=123)
    task_list_id: int = Field(..., description="Task list id", example=123)
    description: str = Field(
        ..., description="Description from task", example="Orlando Salas"
    )
    priority: PriorityEnum = Field(..., description="priority from task", example="low")


class TaskCreate(TaskBase):
    """Schema for creating a new task."""

    user_id: Optional[int] = Field(
        None, description="User ID in charge of the task", example=123
    )

    task_list_id: Optional[int] = Field(
        None, description="Updated task list ID", example=456
    )

    status: Optional[str] = Field(
        TaskStatusEnum.PENDING, description="Updated task status", example=456
    )


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""

    user_id: Optional[int] = Field(
        None, description="Updated user ID in charge of the task", example=123
    )
    task_list_id: Optional[int] = Field(
        None, description="Updated task list ID", example=456
    )
    description: Optional[str] = Field(
        None, description="Updated description of the task", example="Fix login bug"
    )
    priority: Optional[PriorityEnum] = Field(
        None, description="Updated priority of the task", example="high"
    )
    status: Optional[TaskStatusEnum] = Field(
        None, description="Updated task status", example="pending"
    )


class TaskStatusUpdate(BaseModel):
    """Schema for update status from task"""

    status: TaskStatusEnum = Field(
        ..., description="Updated task status", example="pending"
    )


class TaskInChargeUpdate(BaseModel):
    """Schema for update in charge from task"""

    user_id: int = Field(
        ..., description="Updated user ID in charge of the task", example=123
    )


class TaskRead(TaskBase):
    """Schema for reading or returning task data."""

    id: int = Field(..., description="Unique identifier of the task", example=1)

    user_id: Optional[int] = Field(
        None, description="Updated user ID in charge of the task", example=123
    )

    status: TaskStatusEnum = Field(
        ..., description="Indicates status of task.", example="pending"
    )

    model_config = ConfigDict(from_attributes=True)


class TaskListBase(BaseModel):
    """Base schema for a task list."""

    name: str = Field(
        ..., description="Name of the task list", example="Personal Tasks"
    )


class TaskListCreate(TaskListBase):
    """Schema for creating a new task list."""

    user_id: Optional[int] = Field(
        None, description="ID of the user who owns the task list", example=1
    )


class TaskListUpdate(BaseModel):
    """Schema for updating an existing task list."""

    name: Optional[str] = Field(
        None, description="Updated name of the task list", example="Work Tasks"
    )
    user_id: Optional[int] = Field(None, description="Updated user ID", example=2)


class TaskListRead(TaskListBase):
    """Schema for returning task list data."""

    id: int = Field(..., description="Unique identifier of the task list", example=10)
    percentage_of_completeness: Optional[float] = Field(
        0, description="Percentage of completeness fro tasks", example=10.0
    )
    tasks: list[TaskRead] = Field(
        ...,
        description="List of tasks belonging to the task list",
        example=[
            {
                "id": 123,
                "user_id": 123,
                "task_list_id": 456,
                "description": "Descripción from task 1",
                "priority": "low",
                "status": "pending",
            },
        ],
    )

    model_config = ConfigDict(from_attributes=True)


class TaskListWithTasks(BaseModel):
    """Schema for task list with tasks"""

    task_list: TaskListCreate = Field(
        ...,
        description="Data to create task list",
        example={"name": "task list name", "user_id": 123},
    )
    tasks: list[TaskCreate] = Field(
        ...,
        description="List of tasks to create in list",
        example=[
            {
                "title": "Task 1",
                "description": "Descripción from task 1",
                "priority": "low",
            },
            {
                "title": "Task 2",
                "description": "Description from task 2",
                "priority": "mediun",
            },
        ],
    )


class TaskListFilter(BaseModel):
    """Schema for filtering tasks in a task list."""

    status: Optional[TaskStatusEnum] = Field(
        None, description="Filter tasks by status", example=True
    )

    priority: Optional[str] = Field(
        None,
        description="Filter tasks by priority (e.g., low, medium, high)",
        example="high",
    )
