# User Service (SQL Adapter)

This module implements the SQL Service (Component B) from the Social OS architecture guide.

## Overview

The `UserService` class provides a clean abstraction layer for all user-related database operations. It is the **only** component that should write direct SQL queries for users.

## Design Principles

- **Single Responsibility**: All user database logic is encapsulated here
- **RAG-Ready**: The `wiki_content` field is designed to be the primary source for future embedding and retrieval
- **Type Safety**: Uses Pydantic schemas for data validation
- **Error Handling**: Gracefully handles missing records and constraint violations

## Key Methods

### `create_user(db, user_data)`
Creates a new user in the database.
- **Raises**: Exception if `user_id` already exists

### `get_user_by_user_id(db, user_id)`
Retrieves a user by their unique `user_id`.
- **Returns**: User object or None

### `get_all_users(db, skip, limit)`
Retrieves all users with pagination support.
- **Default limit**: 100 users

### `update_user(db, user_id, user_data)`
Updates an existing user (partial update).
- Only updates fields that are provided

### `create_or_update_user(db, user_data)`
Creates a new user or updates if `user_id` already exists.
- **Use case**: Designed for the ingestion pipeline

### `delete_user(db, user_id)`
Deletes a user from the database.
- **Returns**: Boolean indicating success

## Usage Example

```python
from sqlalchemy.orm import Session
from repo_src.backend.adapters.user_service import UserService
from repo_src.backend.data.schemas import UserCreate

# Create a new user
user_data = UserCreate(
    user_id="john_doe",
    name="John Doe",
    bio="Software engineer and coffee enthusiast",
    wiki_content="John has 5 years of experience in Python..."
)

user = UserService.create_user(db, user_data)
```

## Database Schema

The User model includes:
- `id`: Auto-incrementing primary key
- `user_id`: Unique string identifier (indexed)
- `name`: User's display name (indexed)
- `bio`: Short one-line summary
- `wiki_content`: Rich, unstructured text for RAG system
- `created_at`: Timestamp (auto-generated)
- `updated_at`: Timestamp (auto-updated)

## Future Considerations

The `wiki_content` field is specifically designed to support the future RAG-based matchmaking service. When implementing the vector database integration, this field will be:
1. Chunked into smaller segments
2. Embedded using an LLM
3. Stored in a vector database (e.g., ChromaDB)
