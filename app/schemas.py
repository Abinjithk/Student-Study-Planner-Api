from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    name: str
    email: EmailStr
    role: str

    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginSchema(BaseModel):
    email: str
    password: str

class TaskBase(BaseModel):
    title: str
    subject: str
    duration: int = 30
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    subject: Optional[str] = None
    duration: Optional[int] = None
    completed: Optional[bool] = None

class TaskResponse(TaskBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
