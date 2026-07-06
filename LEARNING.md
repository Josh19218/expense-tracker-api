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
