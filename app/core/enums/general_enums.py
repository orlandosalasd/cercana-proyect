from enum import Enum


class PriorityEnum(str, Enum):
    """
    Represents the priority level assigned to a task.

    - `LOW`: Low priority.
    - `MEDIUM`: Medium priority.
    - `HIGH`: High priority.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskStatusEnum(str, Enum):
    """
    Represents the status of a task.
    """

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
