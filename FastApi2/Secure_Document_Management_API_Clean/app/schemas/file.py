from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FileUploadResponse(BaseModel):
    id: int
    filename: str
    stored_filename: str
    size_bytes: int
    mime_type: str
    uploaded_at: datetime
    owner_id: int
    folder_id: Optional[int] = None

    class Config:
        from_attributes = True

class FileResponse(BaseModel):
    id: int
    filename: str
    size_bytes: int
    mime_type: str
    uploaded_at: datetime
    owner_id: int
    folder_id: Optional[int] = None
    share_token: Optional[str] = None
    share_expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True
