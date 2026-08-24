from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime



class UserRegister(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True  # Convert SQLAlchemy object to Pydantic

class NoteCreate(BaseModel):
    title: str
    content: str
    tags: List[str] = []  # Default empty list
    is_favorite: bool = False  # Default False


class NoteUpdate(BaseModel):
    title: str
    content: str
    tags: List[str] = []
    is_favorite: bool = False

class NoteResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    tags: List[str]
    is_favorite: bool
    created_date: datetime
    updated_date: datetime
    
    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"