from pydantic import BaseModel

class TaskCreate(BaseModel):
     title: str
     
class TaskUpdate(BaseModel):
     title: str
     completed: bool
     
class SignupRequest(BaseModel):
     email: str | None = None
     password: str | None = None
     
class LoginRequest(BaseModel):
     email: str | None = None
     password: str | None = None