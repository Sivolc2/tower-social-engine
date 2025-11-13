"""
SQL Service (Data Adapter) for User operations.
This is the only component that should write direct SQL queries for users.
Component B from the architecture guide.
"""

from sqlalchemy.orm import Session
from typing import Optional, List
from repo_src.backend.database.models import User
from repo_src.backend.data.schemas import UserCreate, UserUpdate


class UserService:
    """
    Data adapter for managing User operations in the database.
    All database interaction logic for users is encapsulated here.
    """

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """
        Create a new user in the database.

        Args:
            db: Database session
            user_data: User creation data

        Returns:
            The newly created User object

        Raises:
            Exception: If user_id already exists
        """
        db_user = User(
            user_id=user_data.user_id,
            name=user_data.name,
            bio=user_data.bio,
            wiki_content=user_data.wiki_content
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_user_id(db: Session, user_id: str) -> Optional[User]:
        """
        Retrieve a user by their user_id.

        Args:
            db: Database session
            user_id: The unique user identifier

        Returns:
            User object if found, None otherwise
        """
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Retrieve all users with optional pagination.

        Args:
            db: Database session
            skip: Number of records to skip (default: 0)
            limit: Maximum number of records to return (default: 100)

        Returns:
            List of User objects
        """
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update_user(db: Session, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """
        Update an existing user's information.
        Only updates fields that are provided (not None).

        Args:
            db: Database session
            user_id: The unique user identifier
            user_data: User update data (partial update)

        Returns:
            Updated User object if found, None otherwise
        """
        db_user = UserService.get_user_by_user_id(db, user_id)
        if not db_user:
            return None

        # Only update fields that are provided
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def create_or_update_user(db: Session, user_data: UserCreate) -> User:
        """
        Create a new user or update if user_id already exists.
        This is useful for the ingestion pipeline.

        Args:
            db: Database session
            user_data: User creation data

        Returns:
            The created or updated User object
        """
        existing_user = UserService.get_user_by_user_id(db, user_data.user_id)

        if existing_user:
            # Update existing user
            update_data = UserUpdate(
                name=user_data.name,
                bio=user_data.bio,
                wiki_content=user_data.wiki_content
            )
            return UserService.update_user(db, user_data.user_id, update_data)
        else:
            # Create new user
            return UserService.create_user(db, user_data)

    @staticmethod
    def delete_user(db: Session, user_id: str) -> bool:
        """
        Delete a user from the database.

        Args:
            db: Database session
            user_id: The unique user identifier

        Returns:
            True if user was deleted, False if user was not found
        """
        db_user = UserService.get_user_by_user_id(db, user_id)
        if not db_user:
            return False

        db.delete(db_user)
        db.commit()
        return True
