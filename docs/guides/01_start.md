Of course. This is a wise approach—build the foundational data layer first, ensuring it's perfectly structured to support the more complex AI features later. This minimizes initial complexity and risk.

Here is a detailed implementation and software architecture guide for your development team. It focuses on building the core user profile system (wiki, API, database) while explicitly designing it to be the foundation for a future RAG-based matchmaking service.

---

### **Implementation Guide: Social OS MVP - The RAG-Ready Foundation**

**1. Project Vision & MVP Scope**

The goal of this MVP is to build a robust system for ingesting, storing, and displaying user profile data. While the ultimate aim includes an AI-powered matchmaking service, this initial phase will focus exclusively on creating the foundational data backend and a simple user-facing wiki.

Every architectural decision in this MVP must be made with the future implementation of a Retrieval-Augmented Generation (RAG) system in mind.

**In Scope for MVP:**
*   A backend service to ingest data from local files and populate a user profile database.
*   A SQLite database to store structured user profile information.
*   A RESTful API providing full CRUD (Create, Read, Update, Delete) operations for user profiles.
*   A simple, read-only web frontend (the "Wiki") to display user profiles.
*   A manual trigger mechanism to run the data ingestion pipeline.

**Out of Scope for MVP:**
*   The matchmaking service and its `/match` API endpoint.
*   The Vector Database (e.g., Chroma, FAISS).
*   The text embedding and indexing pipeline.
*   Any real-time RAG or reranking logic.

**2. Core Architecture Philosophy: RAG-Ready**

The architecture is designed around a central principle: **prepare the data correctly now to make future AI integration seamless.** We will use a standard SQL database for structured data but store the rich, descriptive text in a format optimized for future chunking and embedding.

**MVP System Diagram:**

```
                                                     +-----------------------------+
                                                     |  FUTURE: Vector Database &  |
                                                     |     Matchmaking Service     |
                                                     +-----------------------------+
                                                                    ^
                                                                    | (Will read from...)
+-----------------+      +--------------------+      +------------------------------+
| Local Files     |----->|  Data Ingestion &  |----->|  SQLite Database             |
| (Transcripts)   |      |  Processing Core   |      |  (Users Table)               |
+-----------------+      +--------------------+      +------------------------------+
                                                                    ^
                                                                    | (CRUD Operations)
                                                                    v
+-----------------+      +--------------------+      +------------------------------+
| Wiki Frontend   |<---->|  Interactive API   |----->|  SQL Service (Data Adapter)  |
| (Read-Only)     |      |  (GET, POST, PUT)  |      |                              |
+-----------------+      +--------------------+      +------------------------------+
```

**3. Component Breakdown (MVP Focus)**

*   **Component A: Ingestion & Processing Core**
    *   **Responsibility:** Parse raw data and prepare it for storage.
    *   **Tasks:**
        *   Read a specified local text file.
        *   Use an LLM (via OpenRouter) to extract key-value information (e.g., name, bio).
        *   **Crucially, consolidate all descriptive text (skills, project details, interests) into a single, clean text blob.** This blob will be stored in the `wikiContent` field and is the designated source for our future RAG system.
        *   Output a standardized JSON object for a single user.

*   **Component B: SQL Service (Data Adapter)**
    *   **Responsibility:** Manage all communication with the SQLite database. This is the only component that should write direct SQL queries.
    *   **Tasks:**
        *   Establish and manage the connection to the `social_os.db` SQLite file.
        *   Provide high-level functions like `create_or_update_user(user_data)`, `get_user_by_id(user_id)`, `get_all_users()`.
        *   Handle all database logic, including creating the table if it doesn't exist.

*   **Component C: Interactive API**
    *   **Responsibility:** Expose the user data to the outside world, primarily the frontend.
    *   **Tasks:**
        *   Implement a standard RESTful API (e.g., using FastAPI).
        *   Create endpoints for `GET /users`, `GET /users/{id}`, `POST /users`, and `PUT /users/{id}`.
        *   These endpoints will call the functions provided by the **SQL Service (Component B)**.
        *   Implement request/response data validation (e.g., using Pydantic).

*   **Component D: Wiki Frontend**
    *   **Responsibility:** Provide a simple interface for users to view the profiles.
    *   **Tasks:**
        *   On load, call the `GET /users` endpoint to display a list of all users.
        *   Allow clicking on a user to navigate to a detail page that calls `GET /users/{id}`.
        *   Render the `wikiContent` (which can be formatted as Markdown) on the user's detail page.

*   **Component E: Orchestration & Manual Trigger**
    *   **Responsibility:** A top-level script to run the end-to-end ingestion process for testing.
    *   **Tasks:**
        *   Create a command-line script (e.g., `pnpm run ingest-file <filepath>`).
        *   The script will call **Component A** to process the file, then pass the resulting JSON to **Component B** to save it to the database.

**4. Data Architecture: The SQLite Foundation**

The entire system hinges on a well-structured SQLite table.

**`users` table schema:**
```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userId TEXT UNIQUE NOT NULL, -- A stable, machine-readable identifier
    name TEXT NOT NULL,
    bio TEXT,                     -- A short, one-line summary
    -- The single most important field for our future goals.
    -- It holds all rich, unstructured text about the user's skills,
    -- projects, interests, background, etc. This is the "document"
    -- that the future RAG system will chunk and embed.
    wikiContent TEXT,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME
);
```
*   **Implementation Note:** When updating a user, the `updatedAt` timestamp should be automatically set to the current time.

**5. API Contract (MVP)**

| Method | Endpoint | Description | Request Body | Response Body |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/users` | Get a list of all users (summary view). | (None) | `[{"userId", "name", "bio"}]` |
| `GET` | `/users/{userId}` | Get the full profile for a single user. | (None) | `{"userId", "name", "bio", "wikiContent", ...}` |
| `POST`| `/users` | Create a new user profile. | `{"userId", "name", "bio", "wikiContent"}` | `{"status": "success", "data": ...}` |
| `PUT` | `/users/{userId}`| Update an existing user profile. | `{"name"?, "bio"?, "wikiContent"?}` | `{"status": "success", "data": ...}` |

**6. Parallel Development Workstreams**

*   **Workstream 1: Backend Foundation (Data & Ingestion)**
    *   **Focus:** Components A, B, and E.
    *   **Tasks:**
        1.  Implement the **SQL Service (B)** to create the database and table, and provide the core CRUD functions.
        2.  Build the **Ingestion Core (A)** to process a text file and output the standard user JSON.
        3.  Create the **Manual Trigger (E)** script that connects A and B.
    *   **Success Criteria:** A developer can run a single command that successfully parses a file and populates/updates the `social_os.db` file.

*   **Workstream 2: API & Frontend**
    *   **Focus:** Components C and D.
    *   **Tasks:**
        1.  Build the FastAPI application and the API endpoints defined in the **API Contract (Component C)**. Initially, these can return hardcoded mock data.
        2.  Develop the React **Wiki Frontend (D)** to consume this mock API.
        3.  Once Workstream 1 is complete, integrate the API with the **SQL Service (B)**, replacing mock data with live database calls.
    *   **Success Criteria:** The web application is able to display a list of users and their detailed profiles by fetching data from the live backend API.

**7. Path to Future Matchmaking (Post-MVP)**

This architecture provides a clear path forward. To implement the matchmaking service, the following steps will be taken:
1.  **Add a Vector Database:** Introduce a service like ChromaDB.
2.  **Build an Indexing Pipeline:** Create a new service that reads the `wikiContent` from the SQLite DB, chunks it, embeds it via OpenRouter, and stores it in the Vector DB. This can be triggered whenever a user is updated.
3.  **Implement the `/match` Endpoint:** This new endpoint will perform the RAG logic: take a query, embed it, retrieve relevant chunks from the Vector DB, and use an LLM to rerank the results and return a final list of user profiles.