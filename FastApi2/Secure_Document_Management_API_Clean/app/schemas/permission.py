from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ShareFileRequest(BaseModel):
    user_email: EmailStr
    role: str  # "owner", "editor", "viewer"

class PermissionResponse(BaseModel):
    id: int
    file_id: int
    user_id: int
    role: str
    granted_at: datetime

    class Config:
        from_attributes = True

class ShareLinkResponse(BaseModel):
    share_token: str
    share_expires_at: datetime
    public_url: str
