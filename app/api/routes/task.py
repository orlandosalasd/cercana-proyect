from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.task import TaskService, TaskListService
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskRead,
    TaskListRead,
    TaskListCreate,
    TaskStatusUpdate,
    TaskInChargeUpdate,
    TaskListWithTasks,
    TaskListFilter,
)
from app.services.jwt import get_current_user
from app.db.models.user import User
from app.exceptions import TaskDoesNotExists

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/",
)  # response_model=TaskRead)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskRead:
    """Create task.

    Args:
        data (TaskCreate): Task data.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): User from request in JWT.

    Returns:
        TaskRead: Data from created task.
    """
    service = TaskService(db)
    data.user_id = current_user.id
    task = service.create_task(data)
    return task


@router.get("/", response_model=list[TaskRead])
def list_all_tasks(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[TaskRead]:
    """List all task.

    Args:
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): User from request in JWT.

    Returns:
        list[TaskRead]: List of all task.
    """
    service = TaskService(db)
    return service.list_all_tasks()


@router.get("/task-list", response_model=list[TaskListRead])
def list_all_task_lists(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[TaskListRead]:
    """
    Retrieve all task lists for the authenticated user.

    Args:
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Authenticated user from JWT.

    Returns:
        list[TaskListRead]: List of all task lists.
    """
    print("entro")
    service = TaskListService(db)
    return service.list_all_task_lists()


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskRead:
    """Get specific task with id.

    Args:
        task_id (int): Task id.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): User from request in JWT.

    Returns:
        TaskRead: Data from task.
    """
    service = TaskService(db)
    return service.get_task(task_id)


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskRead:
    """Update task with id.

    Args:
        task_id (int): Task id.
        data (TaskUpdate): Data to update from task.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): User from request in JWT.

    Returns:
        TaskRead: Dta from task.
    """
    service = TaskService(db)
    return service.update_task(task_id, data)


@router.delete("/{task_id}", response_model=dict)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Delete Task with id.

    Args:
        task_id (int): Task id to delete.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): User from request in JWT.

    Returns:
        bool:
    """
    service = TaskService(db)
    try:
        service.delete_task(task_id)
        return {"message": "The task was successfully deleted"}
    except TaskDoesNotExists as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/update-status/{task_id}", response_model=TaskRead)
def update_status_task(
    task_id: int,
    data: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskRead:
    """Update status for a task with id.

    Args:
        task_id (int): Task id.
        status (TaskStatusEnum): Status to update from task.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): User from request in JWT.

    Returns:
        TaskRead: Dta from task.
    """
    service = TaskService(db)
    return service.update_task(task_id, TaskUpdate(status=data.status))


@router.patch("/update-in-charge/{task_id}", response_model=TaskRead)
def update_in_charge_task(
    task_id: int,
    data: TaskInChargeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskRead:
    """Update status for a task with id.

    Args:
        task_id (int): Task id.
        status (TaskStatusEnum): Status to update from task.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): User from request in JWT.

    Returns:
        TaskRead: Dta from task.
    """
    service = TaskService(db)
    try:
        return service.update_task(task_id, TaskUpdate(user_id=data.user_id))
    except TaskDoesNotExists as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/task-list", response_model=TaskListRead)
def create_task_list(
    data: TaskListCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskListRead:
    """
    Create a new task list, if user id dont send, the task list will be
    to login/jwt user.

    Args:
        data (TaskListCreate): Task list input data.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Authenticated user from JWT.

    Returns:
        TaskListRead: The created task list.
    """
    if not data.user_id:
        data.user_id = current_user.id
    service = TaskListService(db)
    return service.create_task_list(data)


@router.post("/task-list-with-tasks", response_model=TaskListRead)
def create_task_list_with_tasks(
    data: TaskListWithTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskListRead:
    """
    Create a new task list along with associated tasks.

    Args:
        data (TaskListWithTasks): Task list and task creation data.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Authenticated user from JWT.

    Returns:
        TaskListRead: The created task list with tasks.
    """
    data.task_list.user_id = current_user.id
    service = TaskListService(db)
    return service.create_task_list_with_tasks(data)


@router.get("/task-list/{task_list_id}", response_model=TaskListRead)
def get_task_list(
    task_list_id: int,
    filters: TaskListFilter = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskListRead:
    """
    Retrieve a specific task list by ID, with optional filters for tasks.

    Args:
        task_list_id (int): Task list ID to retrieve.
        filters (TaskListFilter, optional): Optional filters.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Authenticated user from JWT.

    Returns:
        TaskListRead: Task list with filtered tasks and completeness percentage.
    """
    service = TaskListService(db)
    return service.get_task_list(task_list_id, filters)
