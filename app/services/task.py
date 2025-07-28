from sqlalchemy.orm import Session
from app.schemas.task import (
    TaskCreate,
    TaskListCreate,
    TaskListWithTasks,
    TaskRead,
    TaskListRead,
    TaskUpdate,
    TaskListFilter,
)
from app.db.models.task import Task, TaskList
from app.db.repositories.task import TaskRepository, TaskListRepository
from app.exceptions import TaskDoesNotExists, TaskListDoesNotExists
from app.core.enums.general_enums import TaskStatusEnum


class TaskService:
    """Task service class."""

    def __init__(self, db: Session):
        """Contructor of class

        Args:
            db (Session): Database Session.
        """
        self.db = db
        self.task_repository = TaskRepository(db)

    def create_task(self, data: TaskCreate) -> TaskRead:
        """Service to reate task.

        Args:
            db (Session): Database session
            data (TaskCreate): Task data to create

        Returns:
            Task: Task instance
        """
        task = self.task_repository.create(data)
        return TaskRead.model_validate(task, from_attributes=True)

    def get_task(self, task_id: int) -> TaskRead:
        """Service to get task.

        Args:
            db (Session): Database session.
            task_id (int): task id.

        Returns:
            TaskRead: _description_
        """
        task = self.task_repository.get_by_id(task_id)
        return TaskRead.model_validate(task)

    def update_task(self, task_id: int, data: TaskUpdate) -> TaskRead:
        """Service to update task

        Args:
            db (Session): Database session.
            task_id (int): task id.
            data (TaskUpdate): Data from task to update.

        Returns:
            TaskRead: Data from task.
        """
        existing_task = self.task_repository.get_by_id(task_id)
        if not existing_task:
            raise TaskDoesNotExists(task_id)

        previous_assignee = existing_task.user_id
        new_assignee = data.user_id if hasattr(data, "user_id") else None

        updated_task = self.task_repository.update(task_id, data)
        if not updated_task:
            raise TaskDoesNotExists(task_id)

        if new_assignee and new_assignee != previous_assignee:
            print(
                f"Sending invitation email to user ID {new_assignee}, task ID {task_id}"
            )

        return TaskRead.model_validate(updated_task)

    def delete_task(self, task_id: int) -> bool:

        if not self.task_repository.delete(task_id):
            raise TaskDoesNotExists(task_id)
        return True

    def list_all_tasks(self) -> list[TaskRead]:
        """List all tasks.

        Returns:
            list[TaskRead]: List all of tasks.
        """
        tasks = self.task_repository.list_all()
        return [TaskRead.model_validate(task) for task in tasks]


class TaskListService:
    """Task list service class."""

    def __init__(self, db: Session):
        """Contructor of class

        Args:
            db (Session): Database Session.
        """
        self.db = db
        self.task_list_repository = TaskListRepository(db)

    def create_task_list(self, data: TaskListCreate) -> TaskList:
        """create task service.

        Args:
            db (Session): Database session
            data (TaskCreate): Task data to create

        Returns:
            TaskList: TaskList instance
        """
        task_list = self.task_list_repository.create(data)
        return task_list

    def get_task_list(self, task_list_id: int, filters: TaskListFilter) -> TaskListRead:
        """Get tasks list service.

        Args:
            task_list_id (int): Task list id.
            filters (TaskListFilter): Filters to tasks in list of tasks.

        Raises:
            TaskListDoesNotExists: If task list id does not exists.

        Returns:
            TaskListRead: Task list data.
        """

        task_list = self.task_list_repository.get_by_id(task_list_id)
        if not task_list_id:
            raise TaskListDoesNotExists(task_list_id)

        task_query = self.db.query(Task).filter(Task.task_list_id == task_list_id)
        filtered_tasks = task_query.all()
        total = len(filtered_tasks)
        completed_tasks = [
            task for task in filtered_tasks if task.status == TaskStatusEnum.COMPLETED
        ]
        percentage = (len(completed_tasks) / total * 100) if total > 0 else 0

        if filters.priority is not None:
            task_query = task_query.filter(Task.priority == filters.priority)
        if filters.status is not None:
            task_query = task_query.filter(Task.status == filters.status)

        task_list_data = TaskListRead.model_validate(task_list)
        task_list_data.tasks = [TaskRead.model_validate(t) for t in filtered_tasks]
        task_list_data.percentage_of_completeness = percentage

        return task_list_data

    def create_task_list_with_tasks(self, data: TaskListWithTasks) -> TaskListRead:
        """Service to create task list with data.

        Args:
            db (Session): Database session
            data (TaskListWithTasks): Task list with tasks data.

        Returns:
            TaskListRead: Task list data.
        """
        task_service = TaskService(self.db)
        task_list = self.create_task_list(data.task_list)
        for task in data.tasks:
            task.task_list_id = task_list.id
            task = task_service.create_task(task)

        self.db.commit()
        self.db.refresh(task_list)
        return TaskListRead.model_validate(task_list)

    def list_all_task_lists(self) -> list[TaskListRead]:
        """List all task lists including their tasks.

        Returns:
            list[TaskListRead]: List all task lists including their tasks.
        """
        print("entro")
        task_lists = self.task_list_repository.list_all()
        return [
            self.get_task_list(tl.id, TaskListFilter(status=None, priority=None))
            for tl in task_lists
        ]
