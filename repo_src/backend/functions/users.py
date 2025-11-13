"""
SQL Service (Component B) - User CRUD operations
Manages all database operations for user profiles
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from repo_src.backend.database.models import User
from repo_src.backend.data.schemas import UserCreate, UserUpdate


def create_or_update_user(db: Session, user_data: UserCreate) -> User:
    """
    Create a new user or update existing user if user_id already exists.
    This is the primary function for the ingestion pipeline.

    Args:
        db: Database session
        user_data: User data to create or update

    Returns:
        The created or updated User model instance
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.user_id == user_data.user_id).first()

    if existing_user:
        # Update existing user
        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(existing_user, key, value)
        db.commit()
        db.refresh(existing_user)
        return existing_user
    else:
        # Create new user
        db_user = User(**user_data.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """
    Retrieve a single user by their user_id.

    Args:
        db: Database session
        user_id: The unique user identifier

    Returns:
        User model instance or None if not found
    """
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_internal_id(db: Session, id: int) -> Optional[User]:
    """
    Retrieve a single user by their internal database ID.

    Args:
        db: Database session
        id: The internal database ID

    Returns:
        User model instance or None if not found
    """
    return db.query(User).filter(User.id == id).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Retrieve all users from the database.

    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return

    Returns:
        List of User model instances
    """
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: str, user_data: UserUpdate) -> Optional[User]:
    """
    Update an existing user's information.

    Args:
        db: Database session
        user_id: The unique user identifier
        user_data: Updated user data (only provided fields will be updated)

    Returns:
        Updated User model instance or None if not found
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None

    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: str) -> bool:
    """
    Delete a user from the database.

    Args:
        db: Database session
        user_id: The unique user identifier

    Returns:
        True if user was deleted, False if user not found
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True
