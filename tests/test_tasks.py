
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app import database


@pytest.fixture
def client(tmp_path, monkeypatch):

    # Use a separate temporary database for testing
    test_db = tmp_path / "test_tasks.db"

    monkeypatch.setattr(database, "DB_PATH", test_db)

    # Start the application and create the test database
    with TestClient(app) as test_client:
        yield test_client



def create_sample_task(client, title="Learn FastAPI",
                       status="pending", priority="medium"):

    response = client.post(
        "/tasks",
        json={
            "title": title,
            "description": "Task for testing",
            "status": status,
            "priority": priority,
            "due_date": "2026-12-30"
        }
    )

    return response


def test_welcome(client):

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Welcome to Task Management API"
    }


def test_create_task(client):

    response = create_sample_task(client)

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Learn FastAPI"
    assert data["status"] == "pending"
    assert data["priority"] == "medium"
    assert "id" in data




def test_get_all_tasks(client):

    create_sample_task(client, "Task One")
    create_sample_task(client, "Task Two")

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 2




def test_get_task_by_id(client):

    create_response = create_sample_task(client)

    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id



def test_get_nonexistent_task(client):

    response = client.get("/tasks/9999")

    assert response.status_code == 404

    assert response.json()["detail"] == "Task not found"



def test_update_task(client):

    create_response = create_sample_task(client)

    task_id = create_response.json()["id"]

    update_data = {
        "title": "Updated FastAPI Task",
        "description": "Updated description",
        "status": "completed",
        "priority": "high",
        "due_date": "2026-12-31"
    }

    response = client.put(
        f"/tasks/{task_id}",
        json=update_data
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated FastAPI Task"
    assert data["status"] == "completed"
    assert data["priority"] == "high"



def test_patch_task(client):

    create_response = create_sample_task(client)

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "status": "completed"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "completed"

    # Other fields should remain unchanged
    assert data["title"] == "Learn FastAPI"
    assert data["priority"] == "medium"




def test_delete_task(client):

    create_response = create_sample_task(client)

    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200

    assert response.json()["message"] == "Task deleted successfully"

    # Verify that the task no longer exists
    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404




def test_filter_tasks(client):

    create_sample_task(
        client,
        "Completed High Priority",
        "completed",
        "high"
    )

    create_sample_task(
        client,
        "Pending Low Priority",
        "pending",
        "low"
    )

    create_sample_task(
        client,
        "Completed Medium Priority",
        "completed",
        "medium"
    )

    # Filter by status
    response = client.get("/tasks?status=completed")

    assert response.status_code == 200
    assert len(response.json()) == 2

    # Filter by priority
    response = client.get("/tasks?priority=high")

    assert response.status_code == 200
    assert len(response.json()) == 1

    # Filter by both status and priority
    response = client.get(
        "/tasks?status=completed&priority=high"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1



def test_invalid_task_input(client):

    response = client.post(
        "/tasks",
        json={
            "title": "AB",
            "description": "Invalid task",
            "status": "pending",
            "priority": "high"
        }
    )

    assert response.status_code == 422




def test_invalid_status_filter(client):

    response = client.get("/tasks?status=unknown")

    assert response.status_code == 422
