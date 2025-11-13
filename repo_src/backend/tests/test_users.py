"""
Unit tests for user CRUD operations (Component B - SQL Service)
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from repo_src.backend.database.models import Base, User
from repo_src.backend.functions.users import (
    create_or_update_user,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user
)
from repo_src.backend.data.schemas import UserCreate, UserUpdate


@pytest.fixture
def test_db():
    """Create an in-memory SQLite database for testing"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_user(test_db):
    """Test creating a new user"""
    user_data = UserCreate(
        user_id="john_doe",
        name="John Doe",
        bio="A software engineer",
        wiki_content="## Background\n\nJohn is an experienced developer..."
    )

    user = create_or_update_user(test_db, user_data)

    assert user.id is not None
    assert user.user_id == "john_doe"
    assert user.name == "John Doe"
    assert user.bio == "A software engineer"
    assert "John is an experienced developer" in user.wiki_content
    assert user.created_at is not None
    assert user.updated_at is not None


def test_update_existing_user(test_db):
    """Test updating an existing user via create_or_update_user"""
    # Create initial user
    user_data = UserCreate(
        user_id="jane_doe",
        name="Jane Doe",
        bio="Original bio"
    )
    create_or_update_user(test_db, user_data)

    # Update the same user
    updated_data = UserCreate(
        user_id="jane_doe",
        name="Jane Doe",
        bio="Updated bio",
        wiki_content="New content"
    )
    updated_user = create_or_update_user(test_db, updated_data)

    assert updated_user.user_id == "jane_doe"
    assert updated_user.bio == "Updated bio"
    assert updated_user.wiki_content == "New content"


def test_get_user_by_id(test_db):
    """Test retrieving a user by user_id"""
    user_data = UserCreate(
        user_id="test_user",
        name="Test User"
    )
    create_or_update_user(test_db, user_data)

    retrieved_user = get_user_by_id(test_db, "test_user")

    assert retrieved_user is not None
    assert retrieved_user.user_id == "test_user"
    assert retrieved_user.name == "Test User"


def test_get_user_by_id_not_found(test_db):
    """Test retrieving a non-existent user"""
    result = get_user_by_id(test_db, "nonexistent")
    assert result is None


def test_get_all_users(test_db):
    """Test retrieving all users"""
    # Create multiple users
    for i in range(5):
        user_data = UserCreate(
            user_id=f"user_{i}",
            name=f"User {i}"
        )
        create_or_update_user(test_db, user_data)

    all_users = get_all_users(test_db)

    assert len(all_users) == 5
    assert all(isinstance(user, User) for user in all_users)


def test_get_all_users_pagination(test_db):
    """Test pagination in get_all_users"""
    # Create 10 users
    for i in range(10):
        user_data = UserCreate(
            user_id=f"user_{i}",
            name=f"User {i}"
        )
        create_or_update_user(test_db, user_data)

    # Get first 5
    first_page = get_all_users(test_db, skip=0, limit=5)
    assert len(first_page) == 5

    # Get next 5
    second_page = get_all_users(test_db, skip=5, limit=5)
    assert len(second_page) == 5

    # Verify they're different users
    first_ids = [user.user_id for user in first_page]
    second_ids = [user.user_id for user in second_page]
    assert set(first_ids).isdisjoint(set(second_ids))


def test_update_user(test_db):
    """Test updating user fields"""
    # Create a user
    user_data = UserCreate(
        user_id="update_test",
        name="Original Name",
        bio="Original bio"
    )
    create_or_update_user(test_db, user_data)

    # Update specific fields
    update_data = UserUpdate(
        name="Updated Name",
        bio="Updated bio"
    )
    updated_user = update_user(test_db, "update_test", update_data)

    assert updated_user is not None
    assert updated_user.name == "Updated Name"
    assert updated_user.bio == "Updated bio"


def test_update_user_not_found(test_db):
    """Test updating a non-existent user"""
    update_data = UserUpdate(name="New Name")
    result = update_user(test_db, "nonexistent", update_data)
    assert result is None


def test_delete_user(test_db):
    """Test deleting a user"""
    # Create a user
    user_data = UserCreate(
        user_id="delete_test",
        name="To Be Deleted"
    )
    create_or_update_user(test_db, user_data)

    # Verify user exists
    assert get_user_by_id(test_db, "delete_test") is not None

    # Delete user
    result = delete_user(test_db, "delete_test")
    assert result is True

    # Verify user is gone
    assert get_user_by_id(test_db, "delete_test") is None


def test_delete_user_not_found(test_db):
    """Test deleting a non-existent user"""
    result = delete_user(test_db, "nonexistent")
    assert result is False


def test_user_timestamps(test_db):
    """Test that timestamps are set correctly"""
    user_data = UserCreate(
        user_id="timestamp_test",
        name="Timestamp Test"
    )
    user = create_or_update_user(test_db, user_data)

    assert user.created_at is not None
    assert user.updated_at is not None
    # For a new user, created_at and updated_at should be close
    time_diff = abs((user.updated_at - user.created_at).total_seconds())
    assert time_diff < 1  # Less than 1 second difference


def test_unique_user_id_constraint(test_db):
    """Test that user_id uniqueness is enforced at database level"""
    # This test verifies behavior via create_or_update_user
    # which handles duplicates by updating
    user_data1 = UserCreate(
        user_id="unique_test",
        name="First User"
    )
    user_data2 = UserCreate(
        user_id="unique_test",
        name="Second User"
    )

    user1 = create_or_update_user(test_db, user_data1)
    user2 = create_or_update_user(test_db, user_data2)

    # Should be the same database record (same ID)
    assert user1.id == user2.id
    assert user2.name == "Second User"  # Name should be updated
