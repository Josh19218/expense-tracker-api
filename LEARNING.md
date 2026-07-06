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
