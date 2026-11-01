from fastapi import FastAPI, HTTPException , status, Query, Depends
from auth import get_current_user
from schemas import TaskCreate, TaskUpdate, SignupRequest, LoginRequest
from database import get_all_tasks, get_task_by_id, add_task, update_task, delete_task, search_tasks, get_tasks_by_status
from supabase_client import supabase
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


app = FastAPI()
security = HTTPBearer()

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
     
     
@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(user: SignupRequest):

     if user.email is None or user.email.strip() == "" or user.password is None or user.password.strip() == "":
          raise HTTPException(
               status_code=400,
               detail="Email and password are required"
          )

     response = supabase.auth.sign_up({
          "email": user.email,
          "password": user.password
     })

     return response.user
 
 
@app.post("/auth/login")
def login(user: LoginRequest):

     if user.email is None or user.email.strip() == "" or user.password is None or user.password.strip() == "":
          return JSONResponse(
               status_code=400,
               content={"error": "Email and password are required"}
          )

     try:
          response = supabase.auth.sign_in_with_password({
               "email": user.email,
               "password": user.password
          })
     except Exception:
          return JSONResponse(
               status_code=401,
               content={"error": "Invalid login credentials"}
          )

     return {
          "access_token": response.session.access_token,
          "refresh_token": response.session.refresh_token
     }
     


@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    user = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    supabase.auth.sign_out()
    return


@app.get("/public/info")
def public_info():
    return {
        "message": "Welcome stranger! This info is public."
    }
    
    
@app.get("/protected/profile")
def protected_profile(
    user = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }
    


@app.get("/protected/dashboard")
def dashboard(
    user = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return {
        "message": "Welcome to the dashboard",
        "email": user.email
    }
    
    
@app.get("/tasks")
def task(
    search: str | None = Query(None),
    completed: bool | None = Query(None)
):
    if search is not None:
        return search_tasks(search)

    if completed is not None:
        return get_tasks_by_status(completed)

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