from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FolderCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None

class FolderResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    parent_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class FolderUpdate(BaseModel):
    name: str
