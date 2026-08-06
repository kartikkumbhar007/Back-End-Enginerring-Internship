# Task API

A simple FastAPI app for managing tasks.

## Features

- Add, view, update, and delete tasks
- Built with FastAPI and Pydantic
- Has a health check route
- Includes Swagger UI and ReDoc

## Project Structure

- `main.py` - app and routes
- `schemas.py` - request models
- `requirements.txt` - Python packages
- `screenshots/` - example images

## API Endpoints

### `GET /`
Returns basic project info and the main endpoint list.

### `GET /health`
Returns a simple health response:

```json
{
  "status": "ok"
}
```

### `GET /tasks`
Returns all saved tasks.

### `GET /tasks/{id}`
Returns one task by ID.

### `POST /tasks`
Creates a task.

Request body:

```json
{
  "title": "Learn FastAPI"
}
```

New tasks start with `completed: false`.

### `PUT /tasks/{id}`
Updates a task.

Request body:

```json
{
  "title": "Updated task title",
  "completed": true
}
```

### `DELETE /tasks/{id}`
Deletes a task by ID.

## Validation And Behavior

- Task titles cannot be empty.
- Tasks are stored in memory, so they reset when the server restarts.
- `GET /tasks/{id}`, `PUT /tasks/{id}`, and `DELETE /tasks/{id}` return `404` if the task is missing.

## Running The Project

1. Create and activate a virtual environment.
2. Install the packages:

```bash
pip install -r requirements.txt
```

3. Start the server:

```bash
uvicorn main:app --reload
```

4. Open the docs in your browser:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Example Usage

### List tasks

```bash
curl http://127.0.0.1:8000/tasks
```

### Create a task

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Write README\"}"
```

### Update a task

```bash
curl -X PUT http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Learn FastAPI deeply\", \"completed\": true}"
```

### Delete a task

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

## Screenshots

The `screenshots/` folder has example images from the app:

![Create Task](screenshots/Create%20Task.png)

![Delete Task](screenshots/Delete%20task.png)

![Listing Task](screenshots/Listing%20Task.png)

![Swagger UI](screenshots/Swagger%20UI.png)

![Update Task](screenshots/Update%20Task.png)

## Notes

- This project uses in-memory storage only.
- If you want to keep tasks after restart, you can later move them to a database.