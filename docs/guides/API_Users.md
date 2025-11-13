# Users API Documentation

This document describes the RESTful API endpoints for user profile management in the Social OS system.

## Base URL

```
http://localhost:8000
```

## Endpoints

### 1. Get All Users (Summary View)

Retrieves a list of all users with basic information (name, bio, user_id).

**Endpoint**: `GET /users`

**Query Parameters**:
- `skip` (optional, default: 0): Number of records to skip for pagination
- `limit` (optional, default: 100): Maximum number of records to return

**Response**: `200 OK`
```json
[
  {
    "user_id": "john_doe",
    "name": "John Doe",
    "bio": "Software engineer and coffee enthusiast"
  },
  {
    "user_id": "jane_smith",
    "name": "Jane Smith",
    "bio": "Data scientist and machine learning expert"
  }
]
```

**Example cURL**:
```bash
curl http://localhost:8000/users
curl http://localhost:8000/users?skip=0&limit=10
```

---

### 2. Get Single User (Full Profile)

Retrieves the complete profile for a specific user, including wiki content and timestamps.

**Endpoint**: `GET /users/{user_id}`

**Path Parameters**:
- `user_id` (required): The unique user identifier

**Response**: `200 OK`
```json
{
  "user_id": "john_doe",
  "name": "John Doe",
  "bio": "Software engineer and coffee enthusiast",
  "wiki_content": "John has 5 years of experience in Python and JavaScript. He specializes in backend development and has worked on several large-scale distributed systems...",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T15:45:00Z"
}
```

**Error Response**: `404 Not Found`
```json
{
  "detail": "User with user_id 'john_doe' not found"
}
```

**Example cURL**:
```bash
curl http://localhost:8000/users/john_doe
```

---

### 3. Create New User

Creates a new user profile.

**Endpoint**: `POST /users`

**Request Body**:
```json
{
  "user_id": "john_doe",
  "name": "John Doe",
  "bio": "Software engineer and coffee enthusiast",
  "wiki_content": "John has 5 years of experience..."
}
```

**Required Fields**:
- `user_id`: Unique identifier (string)
- `name`: User's display name (string)

**Optional Fields**:
- `bio`: Short one-line summary (string)
- `wiki_content`: Rich descriptive text (string)

**Response**: `201 Created`
```json
{
  "user_id": "john_doe",
  "name": "John Doe",
  "bio": "Software engineer and coffee enthusiast",
  "wiki_content": "John has 5 years of experience...",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Error Response**: `400 Bad Request`
```json
{
  "detail": "User with user_id 'john_doe' already exists"
}
```

**Example cURL**:
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "john_doe",
    "name": "John Doe",
    "bio": "Software engineer",
    "wiki_content": "Experienced developer..."
  }'
```

---

### 4. Update User

Updates an existing user profile. This is a **partial update** - only provided fields will be updated.

**Endpoint**: `PUT /users/{user_id}`

**Path Parameters**:
- `user_id` (required): The unique user identifier

**Request Body** (all fields optional):
```json
{
  "name": "John M. Doe",
  "bio": "Senior Software Engineer",
  "wiki_content": "Updated content..."
}
```

**Response**: `200 OK`
```json
{
  "user_id": "john_doe",
  "name": "John M. Doe",
  "bio": "Senior Software Engineer",
  "wiki_content": "Updated content...",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T15:45:00Z"
}
```

**Error Response**: `404 Not Found`
```json
{
  "detail": "User with user_id 'john_doe' not found"
}
```

**Example cURL**:
```bash
curl -X PUT http://localhost:8000/users/john_doe \
  -H "Content-Type: application/json" \
  -d '{
    "bio": "Senior Software Engineer"
  }'
```

---

### 5. Delete User

Deletes a user profile.

**Endpoint**: `DELETE /users/{user_id}`

**Path Parameters**:
- `user_id` (required): The unique user identifier

**Response**: `204 No Content`

**Error Response**: `404 Not Found`
```json
{
  "detail": "User with user_id 'john_doe' not found"
}
```

**Example cURL**:
```bash
curl -X DELETE http://localhost:8000/users/john_doe
```

---

## Frontend Integration

### React/TypeScript Example

```typescript
// Get all users
const getUsers = async () => {
  const response = await fetch('http://localhost:8000/users');
  const users = await response.json();
  return users;
};

// Get single user
const getUser = async (userId: string) => {
  const response = await fetch(`http://localhost:8000/users/${userId}`);
  if (!response.ok) {
    throw new Error('User not found');
  }
  const user = await response.json();
  return user;
};

// Create user
const createUser = async (userData: {
  user_id: string;
  name: string;
  bio?: string;
  wiki_content?: string;
}) => {
  const response = await fetch('http://localhost:8000/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData),
  });
  if (!response.ok) {
    throw new Error('Failed to create user');
  }
  return await response.json();
};
```

## Testing the API

You can test the API using the interactive documentation at:
```
http://localhost:8000/docs
```

This provides a Swagger UI where you can try all endpoints directly in your browser.

## Database

The API uses SQLite by default. The database file is created at:
```
./app_default.db
```

You can configure a different database by setting the `DATABASE_URL` environment variable.

## CORS Configuration

The API is configured to accept requests from:
- `http://localhost:5173` (default Vite dev server)

If your frontend runs on a different port, update the CORS configuration in `main.py`.
