from sqlalchemy.orm import Session
from app.db.models.task import Task, TaskList
from app.schemas.task import TaskCreate, TaskUpdate, TaskListCreate, TaskListUpdate
from sqlalchemy.orm import selectinload


class TaskRepository:
    """Task class repository."""

    def __init__(self, db: Session) -> None:
        """Constructor class method.

        Args:
            db (Session): Session from database.
        """
        self.db = db

    def create(self, data: TaskCreate) -> Task:
        """Task repository function to create.

        Args:
            data (TaskCreate): Schema to create task.

        Returns:
            Task: Task instance.
        """
        task = Task(**data.model_dump())
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update(self, task_id: int, data: TaskUpdate) -> Task | None:
        """Task repository function to update.

        Args:
            task_id (int): Task id.
            data (TaskUpdate): Schema to update task.

        Returns:
            Task | None: Task instance if exists, otherwise None.
        """
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        """Task repository function to delete.

        Args:
            task_id (int): Task id.

        Returns:
            bool: True if deleted, False if not found.
        """
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False
        self.db.delete(task)
        self.db.commit()
        return True

    def list_all(self) -> list[Task]:
        """List all tasks.

        Returns:
            list[Task]: List of all tasks.
        """
        return self.db.query(Task).all()

    def get_by_id(self, task_id: int) -> Task | None:
        """Task repository function to get task by id.

        Args:
            task_id (int): Task id.

        Returns:
            Task | None: Task instance if exists, otherwise None.
        """
        return self.db.query(Task).filter(Task.id == task_id).first()


class TaskListRepository:
    """TaskList class repository."""

    def __init__(self, db: Session) -> None:
        """Constructor class method.

        Args:
            db (Session): Session from database.
        """
        self.db = db

    def create(self, data: TaskListCreate) -> TaskList:
        """TaskList repository function to create.

        Args:
            data (TaskListCreate): Schema to create task list.

        Returns:
            TaskList: TaskList instance.
        """
        task_list = TaskList(**data.model_dump())
        self.db.add(task_list)
        self.db.commit()
        self.db.refresh(task_list)
        return task_list

    def update(self, list_id: int, data: TaskListUpdate) -> TaskList | None:
        """TaskList repository function to update.

        Args:
            list_id (int): TaskList id.
            data (TaskListUpdate): Schema to update task list.

        Returns:
            TaskList | None: TaskList instance if exists, otherwise None.
        """
        task_list = self.db.query(TaskList).filter(TaskList.id == list_id).first()
        if not task_list:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(task_list, key, value)
        self.db.commit()
        self.db.refresh(task_list)
        return task_list

    def delete(self, list_id: int) -> bool:
        """TaskList repository function to delete.

        Args:
            list_id (int): TaskList id.

        Returns:
            bool: True if deleted, False if not found.
        """
        task_list = self.db.query(TaskList).filter(TaskList.id == list_id).first()
        if not task_list:
            return False
        self.db.delete(task_list)
        self.db.commit()
        return True

    def list_all(self) -> list[TaskList]:
        """List all task lists with their tasks.

        Returns:
            list[TaskList]: List all task lists with their tasks.
        """
        return self.db.query(TaskList).options(selectinload(TaskList.tasks)).all()

    def get_by_id(self, task_list_id: int) -> TaskList | None:
        """TaskList repository function to get task list by id.

        Args:
            list_id (int): TaskList id.

        Returns:
            TaskList | None: TaskList instance if exists, otherwise None.
        """
        task_list = (
            self.db.query(TaskList)
            .options(selectinload(TaskList.tasks))
            .filter(TaskList.id == task_list_id)
            .first()
        )
        return task_list
