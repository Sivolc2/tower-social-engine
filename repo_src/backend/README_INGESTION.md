# User Profile Ingestion System

## Overview

This backend implements the **Workstream 1: Backend Foundation (Data & Ingestion)** from the Social OS MVP specification. It provides a complete data ingestion pipeline for user profiles, designed to be the RAG-ready foundation for future AI-powered matchmaking features.

## Architecture Components

### Component B: SQL Service (`functions/users.py`)
Database adapter providing CRUD operations for user profiles:
- `create_or_update_user()` - Creates new user or updates existing (primary ingestion function)
- `get_user_by_id()` - Retrieve user by user_id
- `get_all_users()` - List all users with pagination
- `update_user()` - Update user information
- `delete_user()` - Remove user from database

### Component A: Ingestion Core (`pipelines/user_ingestion.py`)
LLM-powered data extraction service:
- Reads text files (transcripts, profiles, etc.)
- Uses OpenRouter LLM to extract structured information
- Consolidates all descriptive text into `wiki_content` field (RAG-ready)
- Returns standardized JSON matching the User schema

### Component E: Manual Trigger (`scripts/ingest_user.py`)
CLI orchestration script:
- Command-line interface for running ingestion
- Coordinates Components A and B
- Provides status feedback and error handling

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT UNIQUE NOT NULL,     -- Stable machine-readable identifier
    name TEXT NOT NULL,
    bio TEXT,                          -- Short one-line summary
    wiki_content TEXT,                 -- Rich descriptive text (RAG-ready)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);
```

**Key Design Decision**: The `wiki_content` field is the cornerstone of this system. It contains all rich, unstructured text about the user and is specifically designed to be the source for future RAG (Retrieval-Augmented Generation) chunking and embedding.

## Setup

### Prerequisites
1. Python 3.8+ with dependencies installed:
   ```bash
   pip install -r repo_src/backend/requirements.txt
   ```

2. OpenRouter API key (for LLM extraction):
   ```bash
   # Create a .env file in the project root
   echo "OPENROUTER_API_KEY=your_key_here" >> .env
   echo "OPENROUTER_MODEL_NAME=anthropic/claude-3.5-sonnet" >> .env
   ```

3. Database configuration (optional - defaults to SQLite):
   ```bash
   # Default: sqlite:///./app_default.db
   # Or set custom:
   echo "DATABASE_URL=sqlite:///./social_os.db" >> .env
   ```

## Usage

### Command Line
```bash
# Using pnpm (recommended)
pnpm run ingest-user sample_user_profile.txt

# Or directly with Python
python repo_src/scripts/ingest_user.py sample_user_profile.txt
```

### What Happens During Ingestion

1. **Database Initialization**: Creates tables if they don't exist
2. **File Processing**: Reads the text file
3. **LLM Extraction**: Sends content to OpenRouter LLM for structured extraction
4. **Data Validation**: Validates the extracted JSON against Pydantic schemas
5. **Database Save**: Creates or updates the user in the database
6. **Confirmation**: Displays success message with user details

### Sample Output
```
============================================================
STARTING USER INGESTION
============================================================

Step 1: Ensuring database is ready...
✓ Database tables verified/created

Step 2: Processing file: sample_user_profile.txt
   This will use the LLM to extract user profile data...
✓ Successfully extracted user data for: Sarah Chen
   User ID: sarah_chen
   Bio: Full-stack engineer passionate about AI/ML and building meaningful prod...

Step 3: Saving user profile to database...
✓ Successfully saved/updated user: Sarah Chen
   Database ID: 1
   User ID: sarah_chen
   Created: 2025-11-11 17:30:00
   Updated: 2025-11-11 17:30:00

============================================================
INGESTION COMPLETE
============================================================
```

## Testing

### Manual Testing
A sample user profile is provided at `sample_user_profile.txt`. Test the complete pipeline:

```bash
pnpm run ingest-user sample_user_profile.txt
```

### Programmatic Testing
```python
from repo_src.backend.pipelines.user_ingestion import process_file_sync
from repo_src.backend.functions.users import create_or_update_user, get_all_users
from repo_src.backend.database.connection import SessionLocal
from repo_src.backend.data.schemas import UserCreate

# Process a file
user_data = process_file_sync("path/to/file.txt")

# Save to database
db = SessionLocal()
user_create = UserCreate(**user_data)
db_user = create_or_update_user(db, user_create)

# Retrieve all users
all_users = get_all_users(db)
db.close()
```

## Data Schema

### Input: Text Files
Any text format containing user information:
- Interview transcripts
- Profile documents
- Biographical text
- Resume/CV content

### Output: JSON Structure
```json
{
  "user_id": "john_doe",
  "name": "John Doe",
  "bio": "Software engineer specializing in distributed systems",
  "wiki_content": "## Background\n\nJohn has 10 years...\n\n## Skills\n\n- Python\n- Go\n..."
}
```

## RAG-Ready Design

This system is explicitly designed to support future RAG (Retrieval-Augmented Generation) implementation:

1. **Consolidated Text**: All descriptive information is stored in `wiki_content` as a single, well-formatted document
2. **Clean Markdown**: Content is formatted with headers and structure for easy chunking
3. **Stable IDs**: The `user_id` field provides a stable reference for vector database linkage
4. **Timestamp Tracking**: `created_at` and `updated_at` enable change detection for re-indexing

### Future Integration Path
When implementing the matchmaking service:
1. Add a vector database (ChromaDB, FAISS, Pinecone)
2. Create an indexing pipeline that reads `wiki_content`, chunks it, and stores embeddings
3. Trigger re-indexing on `updated_at` changes
4. Implement `/match` endpoint with RAG retrieval logic

## File Structure
```
repo_src/backend/
├── database/
│   ├── models.py              # User model (SQLAlchemy)
│   ├── connection.py          # Database connection
│   └── setup.py
├── data/
│   └── schemas.py             # Pydantic schemas (UserCreate, UserResponse, etc.)
├── functions/
│   └── users.py               # SQL Service - CRUD operations
├── pipelines/
│   └── user_ingestion.py      # Ingestion Core - LLM extraction
└── scripts/
    └── ingest_user.py         # Manual Trigger - CLI orchestration

repo_src/scripts/
└── ingest_user.py             # CLI entry point

sample_user_profile.txt         # Sample test data
```

## Next Steps (Post-MVP)

This implementation completes **Workstream 1** from the specification. The system is ready for:

**Workstream 2: API & Frontend** (handled by another developer)
- API endpoints will use the functions in `functions/users.py`
- Frontend will display data via these APIs

**Future Enhancements**:
- Vector database integration
- Embedding pipeline for `wiki_content`
- `/match` endpoint for RAG-powered matchmaking
- Batch ingestion for multiple files
- Web upload interface
- Automated re-indexing on updates

## Troubleshooting

### Error: "OPENROUTER_API_KEY not found"
- Ensure `.env` file exists in project root
- Add `OPENROUTER_API_KEY=your_key_here` to `.env`

### Error: "File not found"
- Check file path is correct
- Use absolute path or path relative to project root

### Error: "LLM did not return valid JSON"
- Check OpenRouter API key is valid
- Verify you have API credits
- Try a different model in `.env`: `OPENROUTER_MODEL_NAME=anthropic/claude-3.5-sonnet`

### Database Issues
- Default SQLite database is created automatically
- Check write permissions in project directory
- For custom database, verify `DATABASE_URL` in `.env`

## Success Criteria (from Spec)

✅ **Workstream 1 Complete**: A developer can run a single command that successfully parses a file and populates/updates the database.

```bash
pnpm run ingest-user sample_user_profile.txt
```

This implementation fulfills all requirements for the MVP Backend Foundation.
