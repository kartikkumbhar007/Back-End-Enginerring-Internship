from fastapi import FastAPI, HTTPException , status
from schemas import TaskCreate, TaskUpdate

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
     return tasks



@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")     



@app.post("/tasks",status_code = status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
     
     if task.title.strip() == "":
          raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )
        
     new_task = {
          "id": max(task["id"] for task in tasks) + 1,
          "title": task.title,
          "completed": False,
     }
     
     tasks.append(new_task)
     return new_task



@app.put("/tasks/{id}")
def update_task(id: int, updated_task: TaskUpdate):
     for task in tasks:
          if task["id"] == id:
               task["title"] = updated_task.title
               task["completed"] = updated_task.completed
               return task
          
     raise HTTPException(status_code = 404, detail = "Task Not Found")



@app.delete("/tasks/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_task(id: int):
     for index,task in enumerate(tasks):
          if task["id"] == id:
               tasks.pop(index)
               return
     
     raise HTTPException(status_code= 404, detail = "Task Not Found")
