# Social OS MVP - Integration Guide

## 🎉 Status: FULLY INTEGRATED AND OPERATIONAL

The Social OS MVP is complete with all components working together:
- ✓ Backend API
- ✓ Frontend Wiki
- ✓ Data Ingestion
- ✓ Full end-to-end testing

## Quick Start

```bash
# Start the application
pnpm dev

# Seed test data (in another terminal)
pnpm run seed-users

# Visit the application
open http://localhost:5173
```

## Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:5173 | User wiki interface |
| **Backend API** | http://localhost:8000 | RESTful API |
| **API Docs** | http://localhost:8000/docs | Interactive Swagger UI |

## Documentation Index

### Implementation Guides
1. **[01_start.md](./01_start.md)** - Original architecture specification
2. **[implementation-summary.md](./implementation-summary.md)** - Backend API implementation details
3. **[integration-complete.md](./integration-complete.md)** - Full integration guide (start here!)
4. **[API_Users.md](./API_Users.md)** - API endpoint documentation

### Technical References
- **[backend-api-checklist.md](./backend-api-checklist.md)** - Implementation checklist
- **[data-arch.md](./data-arch.md)** - Data architecture

## Components Overview

### Backend API (Component C)
**Files**:
- `repo_src/backend/routers/users.py` - API endpoints
- `repo_src/backend/adapters/user_service.py` - SQL service
- `repo_src/backend/database/models.py` - User model
- `repo_src/backend/data/schemas.py` - Pydantic schemas

**Features**:
- Full CRUD operations for users
- CamelCase JSON responses
- Pydantic validation
- 11/11 tests passing

### Frontend Wiki (Component D)
**Files**:
- `repo_src/frontend/src/components/UserList.tsx` - User grid
- `repo_src/frontend/src/components/UserDetail.tsx` - Profile view
- `repo_src/frontend/src/App.tsx` - Router

**Features**:
- Responsive grid layout
- Markdown rendering
- React Router navigation
- Error handling

### Data Ingestion (Component A)
**Files**:
- `repo_src/backend/pipelines/user_ingestion.py` - LLM extraction
- `repo_src/scripts/ingest_user.py` - CLI tool
- `repo_src/scripts/seed_test_users.py` - Quick seeding

**Features**:
- LLM-powered data extraction
- Quick seed for development
- Structured JSON output
- Error handling

## Common Commands

```bash
# Development
pnpm dev              # Start frontend + backend
pnpm dev:frontend     # Frontend only
pnpm dev:backend      # Backend only

# Data Management
pnpm seed-users                              # Quick test data
pnpm ingest-user <file>                      # LLM extraction

# Testing
python -m pytest repo_src/backend/tests/test_users_api.py -v

# Cleanup
rm repo_src/backend/app_default.db          # Reset database
lsof -ti:8000 | xargs kill -9               # Kill backend
lsof -ti:5173 | xargs kill -9               # Kill frontend
```

## Sample Data

Three test users are included:
1. **Alice Johnson** - Software engineer specializing in cloud architecture
2. **Robert Chen** - Senior product designer with design systems expertise
3. **Dr. Carol Martinez** - Computational biologist working on genomics

Located in `test_data/`:
- `sample_user_alice.txt`
- `sample_user_bob.txt`
- `sample_user_carol.txt`

## API Examples

### List Users
```bash
curl http://localhost:8000/users
```

Response:
```json
[
  {
    "userId": "alice_johnson",
    "name": "Alice Johnson",
    "bio": "Software engineer and cloud architecture specialist"
  }
]
```

### Get User Detail
```bash
curl http://localhost:8000/users/alice_johnson
```

Response:
```json
{
  "userId": "alice_johnson",
  "name": "Alice Johnson",
  "bio": "Software engineer...",
  "wikiContent": "## Background\n\n...",
  "createdAt": "2025-11-12T01:45:29",
  "updatedAt": "2025-11-12T01:45:29"
}
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│                 User's Browser                  │
│             http://localhost:5173               │
└───────────────────┬─────────────────────────────┘
                    │
                    │ HTTP Requests to /api/users
                    │
┌───────────────────▼─────────────────────────────┐
│           Vite Dev Server (Frontend)            │
│  - UserList.tsx (displays user cards)           │
│  - UserDetail.tsx (shows full profiles)         │
│  - Proxy: /api/* → http://localhost:8000        │
└───────────────────┬─────────────────────────────┘
                    │
                    │ Proxied to backend
                    │
┌───────────────────▼─────────────────────────────┐
│         FastAPI Backend (Backend API)           │
│  - GET /users → list all users                  │
│  - GET /users/{id} → single user detail         │
│  - POST /users → create user                    │
│  - PUT /users/{id} → update user                │
└───────────────────┬─────────────────────────────┘
                    │
                    │ SQLAlchemy ORM
                    │
┌───────────────────▼─────────────────────────────┐
│        SQLite Database (Data Storage)           │
│  File: repo_src/backend/app_default.db          │
│  Table: users                                   │
│  Fields: id, user_id, name, bio, wiki_content   │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│         Data Ingestion (Separate Process)       │
│  - LLM extracts data from text files            │
│  - Transforms to structured JSON                │
│  - Saves to database via SQL Service            │
└─────────────────────────────────────────────────┘
```

## Technology Stack

### Backend
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **Pydantic** - Data validation
- **SQLite** - Database
- **Uvicorn** - ASGI server

### Frontend
- **React** - UI library
- **TypeScript** - Type safety
- **React Router** - Navigation
- **React Markdown** - Content rendering
- **Vite** - Build tool

### Data Pipeline
- **OpenRouter** - LLM API
- **Python asyncio** - Async processing

## Key Integration Points

### 1. Field Naming Convention
- **Database**: snake_case (`user_id`, `wiki_content`)
- **API**: camelCase (`userId`, `wikiContent`)
- **Solution**: Pydantic `serialization_alias`

### 2. API Proxy
- Frontend calls `/api/users`
- Vite proxies to `http://localhost:8000/users`
- Transparent to frontend code

### 3. Database Location
- Located at: `repo_src/backend/app_default.db`
- Important: Run seed from `repo_src/backend` directory

## Troubleshooting

### Issue: Frontend shows "No users found"
**Solution**: Reseed the database
```bash
cd repo_src/backend
pnpm run seed-users
```

### Issue: Port already in use
**Solution**: Kill existing processes
```bash
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:5173 | xargs kill -9  # Frontend
```

### Issue: LLM ingestion fails
**Solution**: Set API key
```bash
export OPENROUTER_API_KEY="your-key"
pnpm run ingest-user <file>
```

### Issue: Database in wrong location
**Solution**: Check and use correct path
```bash
ls repo_src/backend/app_default.db  # Should exist
```

## Next Steps

### Immediate Development
- Add more user profiles
- Enhance UI styling
- Add search/filter functionality
- Implement user editing

### Post-MVP Features
From the original architecture guide:

1. **Vector Database Integration**
   - Add ChromaDB or FAISS
   - Store embeddings of `wikiContent`

2. **RAG Pipeline**
   - Chunk `wikiContent` text
   - Generate embeddings
   - Index in vector DB

3. **Matchmaking Service**
   - Implement `/match` endpoint
   - Query vector DB for similar users
   - LLM-based reranking

## Testing

### Backend Tests
```bash
python -m pytest repo_src/backend/tests/test_users_api.py -v
```
**Result**: ✓ 11/11 passing

### Manual Integration Test
```bash
# 1. Start services
pnpm dev

# 2. Seed data
pnpm seed-users

# 3. Test API
curl http://localhost:8000/users

# 4. Open frontend
open http://localhost:5173

# 5. Verify: Should see 3 user cards
# 6. Click a user: Should see full profile with markdown
```

## Project Structure

```
tower-social-engine/
├── docs/guides/                    # Documentation
│   ├── README_INTEGRATION.md       # This file
│   ├── integration-complete.md     # Detailed integration guide
│   ├── API_Users.md                # API documentation
│   └── ...
├── repo_src/
│   ├── backend/                    # Backend API
│   │   ├── adapters/               # SQL services
│   │   ├── routers/                # API endpoints
│   │   ├── database/               # Models and connection
│   │   ├── data/                   # Pydantic schemas
│   │   ├── pipelines/              # Ingestion logic
│   │   └── app_default.db          # SQLite database
│   ├── frontend/                   # React frontend
│   │   └── src/
│   │       ├── components/         # UI components
│   │       └── App.tsx             # Main app
│   └── scripts/                    # CLI tools
│       ├── ingest_user.py
│       └── seed_test_users.py
├── test_data/                      # Sample transcripts
├── package.json                    # Root commands
└── turbo.json                      # Monorepo config
```

## Support

### Documentation
- Read `integration-complete.md` for detailed setup
- Check `API_Users.md` for endpoint specs
- Review `01_start.md` for architecture

### Common Issues
- Database location problems → see Troubleshooting
- Port conflicts → kill processes and restart
- Missing data → reseed database

## Summary

**The Social OS MVP is fully functional and ready for development!**

- ✅ All components integrated
- ✅ Data flowing end-to-end
- ✅ Tests passing
- ✅ Documentation complete
- ✅ Sample data available
- ✅ Development workflow established

**Start developing**: `pnpm dev` → http://localhost:5173

Happy coding! 🚀
