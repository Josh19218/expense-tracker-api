# Learning Log — Expense Tracker API

## Day 1 — FastAPI Setup & First Endpoint

**What I did:**

- Set up a new project with a virtual environment
- Installed FastAPI and Uvicorn
- Created requirements.txt to track dependencies
- Built my first API endpoint and ran it with Uvicorn
- Viewed FastAPI's auto-generated interactive docs (Swagger UI)

**Commands I learned:**

- python -m venv venv — creates an isolated virtual environment for this project's packages
- source venv/Scripts/activate — activates the virtual environment (Windows/Git Bash)
- pip install fastapi uvicorn — installs the framework and the server that runs it
- pip freeze > requirements.txt — saves exact installed package versions to a file
- uvicorn main:app --reload — runs the API server, auto-restarting on code changes

**Concepts I learned:**

- A virtual environment isolates a project's Python packages from other projects on the same machine
- requirements.txt lets anyone recreate the exact same set of dependencies with one command
- @app.get("/") is a decorator that tells FastAPI which function handles requests to a given URL
- FastAPI automatically converts returned Python dictionaries into JSON responses
- FastAPI auto-generates interactive API docs at /docs, based directly on your code

## Day 2 — POST/GET Endpoints & Pydantic Validation

**What I did:**

- Defined an Expense model using Pydantic's BaseModel
- Built a POST /expenses endpoint to add a new expense
- Built a GET /expenses endpoint to retrieve all expenses
- Tested both endpoints using the Swagger UI at /docs

**Concepts I learned:**

- Pydantic models (class Expense(BaseModel)) define the expected shape of data using type hints
- FastAPI automatically validates incoming request data against a Pydantic model, rejecting bad data with a clear 422 error — no manual try/except needed
- @app.post(...) handles incoming data (like creating something new), @app.get(...) retrieves data
- A function parameter typed as a Pydantic model (expense: Expense) tells FastAPI to parse and validate the request body automatically
- Swagger UI's "Try it out" lets you send real test requests directly from the browser, no separate tool needed

## Day 3 — Connecting a Real Database (SQLite + SQLAlchemy)

**What I did:**

- Installed SQLAlchemy and set up a database connection (database.py)
- Created a SQLAlchemy table model for expenses (models.py)
- Rewrote main.py to read/write expenses to a real SQLite database instead of an in-memory list
- Debugged three real errors: a missing primary key from bad indentation, a typo (autoflus vs autoflush), and a typo (.add() vs .all())

**Concepts I learned:**

- SQLAlchemy is an ORM — it lets you work with database tables using Python classes instead of raw SQL
- A Pydantic model (data shape for the API) and a SQLAlchemy model (actual database table) are different things, even if they represent similar data — hence renaming to ExpenseCreate
- Depends(get_db) is FastAPI's dependency injection system — it runs get_db() and hands the result to the endpoint automatically
- yield inside get_db() pauses the function, lets the endpoint use the database session, then resumes to close it afterward
- db.add() stages a new row, db.commit() saves it, db.refresh() reloads it with its generated ID
- db.query(Model).all() retrieves all rows — different from .add(), which is for creating new rows
- A crashed backend server can look identical to a frozen browser request — checking the terminal, not just the browser, is essential for debugging

## Day 4 — Update & Delete Endpoints (Full CRUD)

**What I did:**

- Built a DELETE /expenses/{expense_id} endpoint
- Built a PUT /expenses/{expense_id} endpoint
- Tested the full CRUD cycle: create, read, update, delete

**Concepts I learned:**

- Path parameters ({expense_id} in the URL) let an endpoint target a specific resource
- FastAPI captures path parameters automatically and validates their type (expense_id: int)
- .filter(Model.column == value).first() is SQLAlchemy's way of finding a single matching row
- Checking if a query result is None before acting on it prevents crashes when an id doesn't exist
- An endpoint can accept both a path parameter and a request body at the same time
- This project now implements full CRUD: Create (POST), Read (GET), Update (PUT), Delete (DELETE) — the standard shape of most real-world APIs

## Day 5 — User Registration & Password Hashing

**What I did:**

- Installed passlib and python-jose for authentication
- Added a User table (username + hashed_password) to the database
- Built hash_password() and verify_password() using bcrypt
- Built a POST /register endpoint that hashes passwords before storing them and rejects duplicate usernames
- Fixed a passlib/bcrypt version compatibility issue by pinning bcrypt==4.0.1

**Concepts I learned:**

- Passwords should never be stored as plain text — hashing is a one-way transformation, so even if the database were leaked, the original password can't be recovered
- bcrypt is a widely-used, secure hashing algorithm for passwords
- verify_password() checks a plain password against a stored hash without ever reversing the hash
- unique=True on a database column enforces that no two rows can have the same value (e.g. no duplicate usernames)
- Package version mismatches between related libraries (passlib and bcrypt here) are a real, common issue — pinning a specific version is a valid fix

## Day 6 — Login & JWT Tokens

**What I did:**

- Built create_access_token() to generate signed JWT tokens
- Built a POST /login endpoint that verifies credentials and returns a token
- Fixed a typo (comma instead of a dot) causing a NameError

**Concepts I learned:**

- A JWT is a signed piece of data (e.g. username + expiry) that proves a user is logged in, without the server needing to check the database on every request
- Tokens are signed with a SECRET_KEY only the server knows — this is a placeholder for now, and must become a real environment variable before deployment
- "sub" is the standard JWT field for identifying who the token belongs to
- Giving a vague "Invalid username or password" error (rather than saying specifically which was wrong) is a deliberate security practice — it avoids revealing whether a username exists
- object.method(...) uses a dot; object,method(...) with a comma creates a tuple instead and causes a NameError when Python tries to call something that isn't there
