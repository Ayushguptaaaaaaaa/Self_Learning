from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.file import File
from app.models.permission import Permission, RoleEnum
from app.schemas.permission import ShareFileRequest, PermissionResponse, ShareLinkResponse

router = APIRouter(prefix="/api/files", tags=["Sharing"])

@router.post("/{file_id}/share", response_model=PermissionResponse)
def share_file(
    file_id: int,
    share_data: ShareFileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Share a file with another user"""
    # Check if file exists
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Only owner can share
    if file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can share this file")

    # Find user to share with
    user_to_share = db.query(User).filter(User.email == share_data.user_email).first()
    if not user_to_share:
        raise HTTPException(status_code=404, detail=f"User with email {share_data.user_email} not found")

    # Check if already shared
    existing_permission = db.query(Permission).filter(
        Permission.file_id == file_id,
        Permission.user_id == user_to_share.id
    ).first()

    if existing_permission:
        # Update role
        existing_permission.role = RoleEnum[share_data.role]
        db.commit()
        db.refresh(existing_permission)
        return existing_permission

    # Create new permission
    new_permission = Permission(
        file_id=file_id,
        user_id=user_to_share.id,
        role=RoleEnum[share_data.role]
    )
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)

    return new_permission

@router.get("/{file_id}/permissions")
def list_permissions(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all users who have access to a file"""
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Only owner can view permissions
    if file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can view permissions")

    permissions = db.query(Permission).filter(Permission.file_id == file_id).all()
    return permissions

@router.delete("/{file_id}/permissions/{user_id}")
def revoke_permission(
    file_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Revoke user's access to a file"""
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Only owner can revoke permissions
    if file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can revoke permissions")

    permission = db.query(Permission).filter(
        Permission.file_id == file_id,
        Permission.user_id == user_id
    ).first()

    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    db.delete(permission)
    db.commit()

    return {"message": "Permission revoked successfully"}

@router.post("/{file_id}/share-link", response_model=ShareLinkResponse)
def create_share_link(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a public share link for a file"""
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Only owner can create share links
    if file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can create share links")

    # Generate token
    share_token = str(uuid.uuid4())
    share_expires_at = datetime.utcnow() + timedelta(days=7)

    # Update file
    file.share_token = share_token
    file.share_expires_at = share_expires_at
    db.commit()

    return {
        "share_token": share_token,
        "share_expires_at": share_expires_at,
        "public_url": f"/api/shared/{share_token}"
    }

@router.delete("/{file_id}/share-link")
def revoke_share_link(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Revoke a public share link"""
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Only owner can revoke share links
    if file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can revoke share links")

    file.share_token = None
    file.share_expires_at = None
    db.commit()

    return {"message": "Share link revoked successfully"}

# Public endpoint - no authentication required
@router.get("/shared/{share_token}")
def access_shared_file(
    share_token: str,
    db: Session = Depends(get_db)
):
    """Access a file via public share link"""
    file = db.query(File).filter(File.share_token == share_token).first()
    if not file:
        raise HTTPException(status_code=404, detail="Invalid or expired share link")

    # Check if link expired
    if file.share_expires_at and file.share_expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Share link has expired")

    from fastapi.responses import FileResponse
    return FileResponse(
        path=file.file_path,
        filename=file.filename,
        media_type=file.mime_type
    )
