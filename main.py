from fastapi import FastAPI, HTTPException , status
from schemas import TaskCreate, TaskUpdate
from database import get_all_tasks, get_task_by_id, add_task, update_task, delete_task


app = FastAPI()

tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "completed": False
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "completed": False
    },
    {
         "id": 3,
         "title": "Write README",
         "completed": True
    }
]

@app.get("/")
def root():
     return { 
             "name" : "Task API",
             "version" : "1.0",
             "endpoints" : ["/tasks"]
     }


@app.get("/health")
def health():
     return { 
             "status" : "ok"
     }
     

@app.get("/tasks")
def task():
     return get_all_tasks()



@app.get("/tasks/{id}")
def get_task(id: int):
    task = get_task_by_id(id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.post("/tasks",status_code = status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
     
     if task.title.strip() == "":
          raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )
        
     return add_task(task.title)


@app.put("/tasks/{id}")
def update_task_route(id: int, updated_task: TaskUpdate):
    task = update_task(
        id,
        updated_task.title,
        updated_task.completed
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task Not Found"
        )

    return task


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_route(id: int):
    task_deleted = delete_task(id)

    if not task_deleted:
        raise HTTPException(
            status_code=404,
            detail="Task Not Found"
        )

    return