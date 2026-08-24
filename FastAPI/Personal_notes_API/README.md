# 📝 Personal Notes API

A secure, full-featured REST API for managing personal notes with user authentication, tagging, searching, and favorites functionality.

---

## 🎯 Project Overview

This is a complete backend API that allows users to:
- ✅ Register and create accounts
- ✅ Login securely with JWT tokens
- ✅ Create, read, update, and delete notes
- ✅ Search notes by title
- ✅ Filter notes by tags
- ✅ Mark notes as favorite
- ✅ Paginate through notes

**Tech Stack:**
- FastAPI (Web Framework)
- SQLAlchemy (Database ORM)
- SQLite (Database)
- Argon2 (Password Hashing)
- JWT (Authentication Tokens)

---

## 🏗️ Architecture & Data Flow

### **How Data Flows Through the System:**

```
User (Browser/Client)
        ↓
    main.py (FastAPI endpoints)
        ↓
  ├─→ schemas.py (Validates incoming data)
  ├─→ auth.py (Handles authentication & password)
  ├─→ models.py (ORM models for database)
  └─→ database.py (Connection to SQLite)
        ↓
    SQLite Database (notes.db)
```

### **Step-by-Step Flow Example:**

**When user creates a note:**

```
1. User sends JSON from browser
         ↓
2. main.py receives POST /notes request
         ↓
3. schemas.py validates the JSON (NoteCreate model)
         ↓
4. auth.py checks the JWT token (get_current_user)
         ↓
5. models.py creates a Note object (ORM model)
         ↓
6. database.py saves to SQLite database
         ↓
7. schemas.py converts response (NoteResponse model)
         ↓
8. main.py sends JSON back to user
```

---

## 📁 File Structure & Descriptions

### **1️⃣ database.py** 
**Purpose:** Sets up the database connection and session management

**What it does:**
- Creates connection to SQLite database
- Sets up the engine (database driver)
- Creates session factory (SessionLocal)
- Provides `get_db()` dependency for FastAPI

**Key Functions/Components:**
- `DATABASE_URL` - SQLite database file path
- `engine` - Connection to database
- `SessionLocal` - Creates new database sessions
- `Base` - Parent class for all ORM models
- `get_db()` - Dependency to inject database session into endpoints

**Why it matters:**
- Without this, API can't talk to database
- Every endpoint uses `get_db()` to access database

---

### **2️⃣ models.py**
**Purpose:** Defines how data is stored in the database (ORM models)

**What it does:**
- Creates User table structure
- Creates Note table structure
- Links User and Note tables (relationships)

**Key Classes/Components:**
- `User` class:
  - `id` - Unique user identifier
  - `username` - Login username (unique)
  - `password_hash` - Encrypted password
  - `email` - User email (unique)
  - `created_at` - Account creation timestamp
  - `notes` - Relationship to user's notes

- `Note` class:
  - `id` - Unique note identifier
  - `user_id` - Foreign key to User (who owns this note)
  - `title` - Note title
  - `content` - Note text
  - `tags` - List of tags (stored as JSON)
  - `is_favorite` - Boolean flag
  - `created_date` - When note was created
  - `updated_date` - When note was last updated
  - `owner` - Relationship back to User

**Why it matters:**
- Defines database schema
- Shows database relationships
- Used by SQLAlchemy to create tables

---

### **3️⃣ schemas.py**
**Purpose:** Validates data coming in and going out of the API

**What it does:**
- Checks that incoming data has correct types
- Ensures required fields are present
- Formats responses for API clients
- Hides sensitive data (like passwords)

**Key Classes/Components:**

**Request Schemas (What user sends):**
- `UserRegister` - Username, password, email for signup
- `UserLogin` - Username, password for login
- `NoteCreate` - Title, content, tags, is_favorite for creating note
- `NoteUpdate` - Same fields for updating note

**Response Schemas (What API sends back):**
- `UserResponse` - Username, email, created_at (NO password!)
- `NoteResponse` - All note fields except user_id (safety)
- `LoginResponse` - access_token, token_type

**Why it matters:**
- Prevents bad data from being saved
- Hides passwords from API responses
- Pydantic automatically converts database objects to JSON

---

### **4️⃣ auth.py**
**Purpose:** Handles all security-related functions

**What it does:**
- Hashes passwords securely
- Creates JWT login tokens
- Verifies tokens are valid
- Extracts user info from tokens

**Key Functions/Components:**

- `SECRET_KEY` - Secret string used to sign tokens (keep safe!)
- `ALGORITHM` - "HS256" (how tokens are signed)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token lasts 30 minutes
- `pwd_context` - Password hashing tool (Argon2)

**Functions:**
- `hash_password(password: str)` - Converts plain password to hash
  - Input: "password123"
  - Output: "$argon2id$v=19$m=65536,t=3,p=4$..." (unreadable)

- `verify_password(plain: str, hashed: str)` - Checks if password matches hash
  - Input: "password123" and hash
  - Output: True or False

- `create_access_token(data: dict)` - Creates JWT token after login
  - Input: {"sub": "rohit"}
  - Output: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." (long token string)

- `verify_token(token: str)` - Checks if token is valid and not expired
  - Input: token string
  - Output: {"sub": "rohit", "exp": 1234567890}
  - Raises error if token is invalid/expired

- `get_current_user(token: str, db: Session)` - FastAPI dependency
  - Gets user from token
  - Used on protected endpoints
  - Ensures only authenticated users can access

**Why it matters:**
- Passwords never stored as plain text
- Tokens expire for security
- Only authenticated users can create/edit/delete notes

---

### **5️⃣ main.py**
**Purpose:** Defines all API endpoints (routes)

**What it does:**
- Creates FastAPI app
- Creates database tables on startup
- Handles all HTTP requests
- Calls other modules to process requests

**Key Components:**

**Initialization:**
- `app = FastAPI()` - Creates the API
- `Base.metadata.create_all()` - Creates tables if they don't exist

**Authentication Endpoints:**

- `POST /auth/register` - User signup
  - Input: UserRegister (username, password, email)
  - Process: Hash password → Check if user exists → Save to DB
  - Output: UserResponse (user info, no password)
  - Status: 201 Created

- `POST /auth/login` - User login
  - Input: UserLogin (username, password)
  - Process: Find user → Verify password → Create token
  - Output: LoginResponse (access_token)
  - Status: 200 OK

**Note Endpoints (All require authentication):**

- `POST /notes` - Create new note
  - Input: NoteCreate + token
  - Process: Validate token → Convert tags to JSON → Save
  - Output: NoteResponse
  - Status: 201 Created

- `GET /notes` - Get all notes for current user
  - Input: token + optional query params (search, tag, limit, offset)
  - Process: Get user from token → Query notes → Filter/paginate
  - Output: List of NoteResponse
  - Status: 200 OK

- `GET /notes/{note_id}` - Get single note
  - Input: note_id + token
  - Process: Find note → Check ownership → Return
  - Output: NoteResponse
  - Status: 200 OK or 404 Not Found

- `PUT /notes/{note_id}` - Update note
  - Input: note_id + NoteUpdate + token
  - Process: Find note → Check ownership → Update → Save
  - Output: NoteResponse
  - Status: 200 OK

- `DELETE /notes/{note_id}` - Delete note
  - Input: note_id + token
  - Process: Find note → Check ownership → Delete
  - Output: {"message": "Note deleted successfully"}
  - Status: 200 OK

**Why it matters:**
- This is the public API interface
- All data flows through these endpoints
- Orchestrates database, auth, and validation

---

## 🔄 Complete Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER/CLIENT (Browser)                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
          ┌──────────────────────────────┐
          │      main.py                 │
          │  (API Endpoints)             │
          └──────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ↓               ↓               ↓
    ┌─────────┐   ┌───────────┐   ┌──────────┐
    │schemas.py│   │ auth.py   │   │models.py │
    │(Validate)│   │(Secure)   │   │(Storage) │
    └─────────┘   └───────────┘   └──────────┘
         │               │               │
         └───────────────┼───────────────┘
                         ↓
          ┌──────────────────────────────┐
          │   database.py                │
          │  (SQLAlchemy Engine)         │
          └──────────────────────────────┘
                         │
                         ↓
          ┌──────────────────────────────┐
          │    notes.db (SQLite)         │
          │  ┌──────────────────────┐    │
          │  │ Users Table          │    │
          │  ├──────────────────────┤    │
          │  │ Notes Table          │    │
          │  └──────────────────────┘    │
          └──────────────────────────────┘
```

---

## 🚀 How to Use

### **Installation:**
```bash
pip install -r requirements.txt
```

### **Run Server:**
```bash
uvicorn main:app --reload
```

### **Access API:**
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

---

## 🔐 Security Features

✅ **Password Hashing** - Argon2 algorithm (industry standard)
✅ **JWT Tokens** - Expire after 30 minutes
✅ **User Isolation** - Users can only access their own notes
✅ **Token Verification** - Every protected endpoint checks token
✅ **SQL Injection Prevention** - SQLAlchemy uses parameterized queries
✅ **Type Validation** - Pydantic validates all input data

---

## 📊 Database Schema

### **Users Table:**
| Field | Type | Constraint |
|-------|------|-----------|
| id | Integer | PRIMARY KEY |
| username | String | UNIQUE |
| password_hash | String | NOT NULL |
| email | String | UNIQUE |
| created_at | DateTime | DEFAULT NOW |

### **Notes Table:**
| Field | Type | Constraint |
|-------|------|-----------|
| id | Integer | PRIMARY KEY |
| user_id | Integer | FOREIGN KEY (users.id) |
| title | String | NOT NULL |
| content | Text | NOT NULL |
| tags | Text | JSON format |
| is_favorite | Boolean | DEFAULT False |
| created_date | DateTime | DEFAULT NOW |
| updated_date | DateTime | DEFAULT NOW |

---

## 📝 Example Requests & Responses

### **Register User:**
```json
POST /auth/register
{
  "username": "rohit",
  "password": "password123",
  "email": "rohit@gmail.com"
}

Response (201):
{
  "id": 1,
  "username": "rohit",
  "email": "rohit@gmail.com",
  "created_at": "2024-08-23T10:30:00"
}
```

### **Login:**
```json
POST /auth/login
{
  "username": "rohit",
  "password": "password123"
}

Response (200):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### **Create Note:**
```json
POST /notes
Header: token = "eyJhbGciOi..."

{
  "title": "Learn FastAPI",
  "content": "Study async patterns",
  "tags": ["python", "fastapi"],
  "is_favorite": true
}

Response (201):
{
  "id": 1,
  "user_id": 1,
  "title": "Learn FastAPI",
  "content": "Study async patterns",
  "tags": ["python", "fastapi"],
  "is_favorite": true,
  "created_date": "2024-08-23T10:35:00",
  "updated_date": "2024-08-23T10:35:00"
}
```

---

## 🎓 Learning Outcomes

By building this project, you learned:

✅ **FastAPI** - Modern web framework
✅ **SQLAlchemy ORM** - Database object-relational mapping
✅ **Authentication** - JWT tokens & password hashing
✅ **API Design** - REST principles
✅ **Database Design** - Relationships & constraints
✅ **Security** - Input validation, token verification, user isolation
✅ **Error Handling** - HTTPException and custom responses

---

## 📚 Project Files Summary

| File | Lines | Purpose |
|------|-------|---------|
| database.py | ~20 | Database connection setup |
| models.py | ~35 | ORM models (User, Note) |
| schemas.py | ~50 | Pydantic validation models |
| auth.py | ~80 | Authentication functions |
| main.py | ~200 | API endpoints |
| **Total** | **~385** | Complete API |

---

## 🎉 Conclusion

This Personal Notes API demonstrates a complete, production-ready backend system with:
- Secure user authentication
- Database persistence
- Data validation
- REST API best practices
- Clean code architecture

**Ready for Phase 2?** Start building more advanced features! 🚀
