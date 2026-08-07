<div align="center">

# Task API

A simple database-backed CRUD API built with FastAPI and SQLite.

<p>
	<img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white" alt="FastAPI">
	<img src="https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white" alt="SQLite">
</p>

</div>

---

## About

This project is a simple Task CRUD API built as part of a backend engineering internship assignment.

The API started with in-memory task storage and was later connected to SQLite. Tasks can now be created, viewed, updated, and deleted while remaining persistent across server restarts.

---

## Features

- Create, read, update, and delete tasks
- SQLite database for persistent storage
- SQL-based task search
- Filter tasks by completion status
- Pydantic request validation
- Parameterized SQL queries
- Empty task title validation
- HTTP status code handling
- Health check endpoint
- Interactive Swagger UI
- ReDoc API documentation

---

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLite
- Uvicorn

---

## Project Structure

```text
.
├── main.py
├── database.py
├── schemas.py
├── requirements.txt
├── screenshots/
└── tasks.db
```

| File / Folder | Description |
| --- | --- |
| main.py | FastAPI application and API routes |
| database.py | SQLite connection and database operations |
| schemas.py | Pydantic request models |
| requirements.txt | Project dependencies |
| screenshots/ | Screenshots of the API and SQLite work |
| tasks.db | Local SQLite database file |

> tasks.db is a local database file and should be ignored by Git.

---

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | Returns basic API information |
| GET | `/health` | Health check |
| GET | `/tasks` | Returns all tasks |
| GET | `/tasks/{id}` | Returns one task |
| POST | `/tasks` | Creates a new task |
| PUT | `/tasks/{id}` | Updates an existing task |
| DELETE | `/tasks/{id}` | Deletes a task |
| GET | `/tasks?search=FastAPI` | Searches tasks by title |
| GET | `/tasks?completed=true` | Returns completed tasks |
| GET | `/tasks?completed=false` | Returns incomplete tasks |
---

## Example Request

### Create a Task

```json
{
	"title": "Learn FastAPI"
}
```

New tasks are created with:

```json
{
	"completed": false
}
```

### Update a Task

```json
{
	"title": "Learn FastAPI deeply",
	"completed": true
}
```

---

## Database

This project uses **SQLite** for task storage.

SQLite was chosen because:

- The database is stored in a single file.
- It does not require a separate database server.
- Data survives when the FastAPI server is stopped and started again.

The database file is:

```text
tasks.db
```

The `tasks` table is created automatically when the application starts.

If the table is empty, the application inserts three seed tasks:

1. Learn FastAPI
2. Build CRUD API
3. Write README

### Table Schema

| Column | Type | Description |
| --- | --- | --- |
| id | INTEGER | Primary key with auto-increment |
| title | TEXT | Task title |
| completed | BOOLEAN | Task completion status |

---

## Validation and Behavior

- Empty or whitespace-only task titles return HTTP `400`.
- Missing task IDs return HTTP `404`.
- Successful task creation returns HTTP `201 Created`.
- Successful task deletion returns HTTP `204 No Content`.
- Tasks persist across server restarts.
- SQL queries use parameterized placeholders instead of string concatenation.

---

## Exploring SQLite

DB Browser for SQLite was used to execute SQL directly against the `tasks.db` file.

Example query:

```sql
SELECT * FROM tasks WHERE completed = 1;
```

This returns only completed tasks.

The database was also updated manually using:

```sql
UPDATE tasks SET completed = 1;
```

After saving the database change in DB Browser for SQLite, the API reflected the updated `completed` values through `GET /tasks` without restarting FastAPI.

This demonstrated that the API and DB Browser for SQLite were reading the same database file.

---

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Server

```bash
uvicorn main:app --reload
```

### 3. Open API Documentation

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## Example Usage

### List Tasks

```bash
curl http://127.0.0.1:8000/tasks
```

### Create a Task

```bash
curl -X POST http://127.0.0.1:8000/tasks \
	-H "Content-Type: application/json" \
	-d "{\"title\": \"Write README\"}"
```

### Update a Task

```bash
curl -X PUT http://127.0.0.1:8000/tasks/1 \
	-H "Content-Type: application/json" \
	-d "{\"title\": \"Learn FastAPI deeply\", \"completed\": true}"
```

### Delete a Task

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```
---

## Optional SQL Features

Tasks can also be searched and filtered directly through SQL queries.

### Search Tasks

```text
GET /tasks?search=FastAPI
```
Uses SQL `LIKE` to search task titles.

### Filter by Completion Status

```text
GET /tasks?completed=true
GET /tasks?completed=false
```
Uses a SQL `WHERE completed = ?` condition to return tasks by their completion status.

---

## Screenshots

### Assignment 1 API

![Create Task](screenshots/Create%20Task.png)

![Delete Task](screenshots/Delete%20task.png)

![Listing Task](screenshots/Listing%20Task.png)

![Swagger UI](screenshots/Swagger%20UI.png)

![Update Task](screenshots/Update%20Task.png)

### Stage 4: Exploring SQLite

![Database Update](screenshots/Database%20Update.png)

![API Reflects Database Change](screenshots/API%20Reflects%20Database%20Change.png)

---

## What I Learned

- Building REST API endpoints with FastAPI
- Using Pydantic for request validation
- Performing CRUD operations with SQLite
- Using parameterized SQL queries
- Using SQL `LIKE` and `WHERE` clauses for database-level filtering
- Understanding database persistence across server restarts
- Testing APIs using Swagger UI and command-line requests
- Exploring and modifying a SQLite database directly using DB Browser for SQLite
