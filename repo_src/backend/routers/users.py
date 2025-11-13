"""
Interactive API (Component C) for User operations.
RESTful API endpoints that expose user data to the frontend.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from repo_src.backend.database.connection import get_db
from repo_src.backend.data.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserSummary
)
from repo_src.backend.adapters.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[UserSummary], response_model_by_alias=True)
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get a list of all users (summary view).
    Returns only userId, name, and bio for each user.

    Args:
        skip: Number of records to skip for pagination (default: 0)
        limit: Maximum number of records to return (default: 100)
        db: Database session (injected)

    Returns:
        List of user summaries
    """
    users = UserService.get_all_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserResponse, response_model_by_alias=True)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get the full profile for a single user.
    Includes all fields including wikiContent and timestamps.

    Args:
        user_id: The unique user identifier
        db: Database session (injected)

    Returns:
        Full user profile

    Raises:
        HTTPException: 404 if user not found
    """
    user = UserService.get_user_by_user_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with user_id '{user_id}' not found"
        )
    return user


@router.post("", response_model=UserResponse, response_model_by_alias=True, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user profile.

    Args:
        user_data: User creation data
        db: Database session (injected)

    Returns:
        The newly created user profile

    Raises:
        HTTPException: 400 if user_id already exists
    """
    # Check if user already exists
    existing_user = UserService.get_user_by_user_id(db, user_data.user_id)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with user_id '{user_data.user_id}' already exists"
        )

    try:
        new_user = UserService.create_user(db, user_data)
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


@router.put("/{user_id}", response_model=UserResponse, response_model_by_alias=True)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing user profile.
    Only updates fields that are provided (partial update).

    Args:
        user_id: The unique user identifier
        user_data: User update data (partial)
        db: Database session (injected)

    Returns:
        The updated user profile

    Raises:
        HTTPException: 404 if user not found
    """
    updated_user = UserService.update_user(db, user_id, user_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with user_id '{user_id}' not found"
        )
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a user profile.
    Not part of the MVP spec, but useful for testing and management.

    Args:
        user_id: The unique user identifier
        db: Database session (injected)

    Raises:
        HTTPException: 404 if user not found
    """
    success = UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with user_id '{user_id}' not found"
        )
    return None
