import pytest


@pytest.mark.integration
def test_create_task(client, header_user_token):
    """Test create task route."""

    response = client.post(
        "tasks/task-list/", headers=header_user_token, json={"name": "test_list_task"}
    )

    task_list_data = response.json()
    response = client.post(
        "tasks/",
        headers=header_user_token,
        json={
            "task_list_id": task_list_data["id"],
            "description": "test task description 1",
            "priority": "low",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["task_list_id"] == task_list_data["id"]
    assert data["priority"] == "low"


@pytest.mark.integration
def test_create_task_list_with_tasks(client, header_user_token):
    """Test creating a task list along with its tasks."""

    payload = {
        "task_list": {"name": "Test Task List With Tasks"},
        "tasks": [
            {"description": "Task 1 description", "priority": "low"},
            {"description": "Task 2 description", "priority": "high"},
        ],
    }

    response = client.post(
        "tasks/task-list-with-tasks", headers=header_user_token, json=payload
    )

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == payload["task_list"]["name"]
    assert len(data["tasks"]) == 2
    assert data["tasks"][0]["description"] == "Task 1 description"
    assert data["tasks"][1]["priority"] == "high"


@pytest.mark.integration
def test_list_all_tasks(client, header_user_token):
    """Test list all task route"""
    payload = {
        "task_list": {"name": "Test Task List With Tasks"},
        "tasks": [
            {"description": "list task 1", "priority": "low"},
            {"description": "list task 2", "priority": "high"},
        ],
    }

    client.post("tasks/task-list-with-tasks", headers=header_user_token, json=payload)

    response = client.get("/tasks/", headers=header_user_token)

    assert response.status_code == 200
    data = response.json()

    descriptions = [t["description"] for t in data]
    assert "list task 1" in descriptions
    assert "list task 2" in descriptions


@pytest.mark.integration
def test_get_task(client, header_user_token):
    """Test get task route."""

    response = client.post(
        "tasks/task-list/",
        headers=header_user_token,
        json={"name": "test get task list task"},
    )

    task_list_data = response.json()
    response = client.post(
        "tasks/",
        headers=header_user_token,
        json={
            "task_list_id": task_list_data["id"],
            "description": "test task description 1",
            "priority": "low",
        },
    )

    data = response.json()
    response = client.get(f"tasks/{data["id"]}", headers=header_user_token)
    assert response.json()["id"] == data["id"]


@pytest.mark.integration
def test_put_task(client, header_user_token):
    """Test put task route."""

    response = client.post(
        "tasks/task-list/",
        headers=header_user_token,
        json={"name": "test get task list task"},
    )

    task_list_data = response.json()
    response = client.post(
        "tasks/",
        headers=header_user_token,
        json={
            "task_list_id": task_list_data["id"],
            "description": "test task description 1",
            "priority": "low",
        },
    )

    data = response.json()
    response = client.put(
        f"tasks/{data["id"]}",
        headers=header_user_token,
        json={"description": "test task description update", "priority": "high"},
    )

    assert response.json()["id"] == data["id"]
    assert response.json()["description"] == "test task description update"
    assert response.json()["priority"] == "high"


@pytest.mark.integration
def test_delete_task(client, header_user_token):
    """Test delete task route."""

    response = client.post(
        "tasks/task-list/",
        headers=header_user_token,
        json={"name": "test get task list task"},
    )

    task_list_data = response.json()
    response = client.post(
        "tasks/",
        headers=header_user_token,
        json={
            "task_list_id": task_list_data["id"],
            "description": "test task description 1",
            "priority": "low",
        },
    )

    data = response.json()
    response = client.delete(f"tasks/{data["id"]}", headers=header_user_token)

    success_message = "The task was successfully deleted"
    assert response.json()["message"] == success_message

    response = client.delete(f"tasks/{123456}", headers=header_user_token)

    assert response.status_code == 400


@pytest.mark.integration
def test_update_status_task(client, header_user_token):
    """Test update status task route."""

    response = client.post(
        "tasks/task-list/",
        headers=header_user_token,
        json={"name": "test get task list task"},
    )

    task_list_data = response.json()
    response = client.post(
        "tasks/",
        headers=header_user_token,
        json={
            "task_list_id": task_list_data["id"],
            "description": "test task description 1",
            "priority": "low",
        },
    )

    data = response.json()
    response = client.patch(
        f"tasks/update-status/{data["id"]}",
        headers=header_user_token,
        json={"status": "in_progress"},
    )

    assert response.json()["id"] == data["id"]
    assert response.json()["status"] == "in_progress"


@pytest.mark.integration
def test_update_in_charge_task(client, header_user_token):
    """Test update in charge task route."""

    response = client.post(
        "tasks/task-list/",
        headers=header_user_token,
        json={"name": "test get task list task"},
    )

    task_list_data = response.json()
    response = client.post(
        "tasks/",
        headers=header_user_token,
        json={
            "task_list_id": task_list_data["id"],
            "description": "test task description 1",
            "priority": "low",
        },
    )
    data = response.json()

    response = client.post(
        "/auth/register",
        json={
            "email": "test_in_charge_update@example.com",
            "password": "123456",
            "full_name": "Test User",
        },
    )
    user_id = response.json()["id"]
    response = client.patch(
        f"tasks/update-in-charge/{data["id"]}",
        headers=header_user_token,
        json={"user_id": user_id},
    )

    assert response.json()["id"] == data["id"]
    assert response.json()["user_id"] == user_id

    response = client.patch(
        f"tasks/update-in-charge/{1234567}",
        headers=header_user_token,
        json={"user_id": user_id},
    )

    assert response.status_code == 400


@pytest.mark.integration
def test_list_all_task_list(client, header_user_token):
    """Test list all task route"""

    payload_a = {
        "task_list": {"name": "Test Task List With Tasks 1"},
        "tasks": [
            {"description": "list task 1", "priority": "low"},
            {"description": "list task 2", "priority": "high"},
        ],
    }
    payload_b = {
        "task_list": {"name": "Test Task List With Tasks 2"},
        "tasks": [
            {"description": "list task 3", "priority": "low"},
            {"description": "list task 4", "priority": "high"},
        ],
    }

    client.post("tasks/task-list-with-tasks", headers=header_user_token, json=payload_a)
    client.post("tasks/task-list-with-tasks", headers=header_user_token, json=payload_b)

    response = client.get("tasks/task-list", headers=header_user_token)
    assert response.status_code == 200
    data = response.json()
    names = [t["name"] for t in data]
    assert "Test Task List With Tasks 1" in names
    assert "Test Task List With Tasks 2" in names


@pytest.mark.integration
def test_get_task_list(client, header_user_token):
    """Test get task list route"""

    payload = {
        "task_list": {"name": "Test get Task List 1"},
        "tasks": [
            {"description": "list task 1", "priority": "low", "status": "completed"},
            {"description": "list task 2", "priority": "high", "status": "pending"},
        ],
    }

    response = client.post(
        "tasks/task-list-with-tasks", headers=header_user_token, json=payload
    )

    task_list_id = response.json()["id"]
    response = client.get(f"tasks/task-list/{task_list_id}", headers=header_user_token)
    assert response.status_code == 200
    data = response.json()
    assert data["percentage_of_completeness"] == 50
