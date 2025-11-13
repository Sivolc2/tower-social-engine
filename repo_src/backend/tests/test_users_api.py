"""
Tests for the Users API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from repo_src.backend.main import app
from repo_src.backend.database.connection import Base, get_db
from repo_src.backend.database.models import User

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override the get_db dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Reset the database before each test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_user():
    """Test creating a new user."""
    user_data = {
        "user_id": "john_doe",
        "name": "John Doe",
        "bio": "Software engineer",
        "wiki_content": "John has 5 years of experience in Python"
    }

    response = client.post("/users", json=user_data)
    assert response.status_code == 201

    data = response.json()
    assert data["userId"] == "john_doe"
    assert data["name"] == "John Doe"
    assert data["bio"] == "Software engineer"
    assert "createdAt" in data
    assert "updatedAt" in data


def test_create_duplicate_user():
    """Test that creating a duplicate user fails."""
    user_data = {
        "user_id": "john_doe",
        "name": "John Doe",
    }

    # Create first user
    response = client.post("/users", json=user_data)
    assert response.status_code == 201

    # Try to create duplicate
    response = client.post("/users", json=user_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_get_all_users():
    """Test getting all users."""
    # Create two users
    client.post("/users", json={"user_id": "user1", "name": "User One"})
    client.post("/users", json={"user_id": "user2", "name": "User Two"})

    response = client.get("/users")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["userId"] in ["user1", "user2"]
    assert "wikiContent" not in data[0]  # Summary view doesn't include wikiContent


def test_get_user_by_id():
    """Test getting a single user by ID."""
    # Create a user
    client.post("/users", json={
        "user_id": "john_doe",
        "name": "John Doe",
        "bio": "Software engineer",
        "wiki_content": "Detailed content"
    })

    response = client.get("/users/john_doe")
    assert response.status_code == 200

    data = response.json()
    assert data["userId"] == "john_doe"
    assert data["name"] == "John Doe"
    assert data["wikiContent"] == "Detailed content"
    assert "createdAt" in data


def test_get_nonexistent_user():
    """Test getting a user that doesn't exist."""
    response = client.get("/users/nonexistent")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_update_user():
    """Test updating an existing user."""
    # Create a user
    client.post("/users", json={
        "user_id": "john_doe",
        "name": "John Doe",
        "bio": "Software engineer"
    })

    # Update the user
    update_data = {
        "name": "John M. Doe",
        "bio": "Senior Software Engineer"
    }
    response = client.put("/users/john_doe", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "John M. Doe"
    assert data["bio"] == "Senior Software Engineer"


def test_update_nonexistent_user():
    """Test updating a user that doesn't exist."""
    update_data = {"name": "New Name"}
    response = client.put("/users/nonexistent", json=update_data)
    assert response.status_code == 404


def test_delete_user():
    """Test deleting a user."""
    # Create a user
    client.post("/users", json={
        "user_id": "john_doe",
        "name": "John Doe"
    })

    # Delete the user
    response = client.delete("/users/john_doe")
    assert response.status_code == 204

    # Verify user is deleted
    response = client.get("/users/john_doe")
    assert response.status_code == 404


def test_delete_nonexistent_user():
    """Test deleting a user that doesn't exist."""
    response = client.delete("/users/nonexistent")
    assert response.status_code == 404


def test_pagination():
    """Test pagination of user list."""
    # Create 5 users
    for i in range(5):
        client.post("/users", json={
            "user_id": f"user{i}",
            "name": f"User {i}"
        })

    # Get first 2 users
    response = client.get("/users?skip=0&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2

    # Get next 2 users
    response = client.get("/users?skip=2&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_partial_update():
    """Test that partial updates only change specified fields."""
    # Create a user
    client.post("/users", json={
        "user_id": "john_doe",
        "name": "John Doe",
        "bio": "Software engineer",
        "wiki_content": "Original content"
    })

    # Update only the bio
    response = client.put("/users/john_doe", json={"bio": "Senior Engineer"})
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "John Doe"  # Unchanged
    assert data["bio"] == "Senior Engineer"  # Updated
    assert data["wikiContent"] == "Original content"  # Unchanged
