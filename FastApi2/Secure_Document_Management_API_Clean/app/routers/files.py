from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import require_file_permission
from app.models.user import User
from app.models.file import File as FileModel
from app.schemas.file import FileUploadResponse, FileResponse
from app.utils.file_handler import save_upload_file, delete_file
from app.utils.validators import validate_file_size, validate_file_extension

router = APIRouter(prefix="/api/files", tags=["Files"])

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    folder_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a new file"""
    # Validate file
    validate_file_extension(file.filename)
    size_bytes = validate_file_size(file)

    # Save file to disk
    stored_filename, file_path, size_bytes, mime_type = save_upload_file(file)

    # Save metadata to database
    new_file = FileModel(
        filename=file.filename,
        stored_filename=stored_filename,
        file_path=file_path,
        size_bytes=size_bytes,
        mime_type=mime_type,
        owner_id=current_user.id,
        folder_id=folder_id
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return new_file

@router.get("/{file_id}", response_model=FileResponse)
def get_file_metadata(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get file metadata"""
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    require_file_permission(db, current_user, file, "viewer")

    return file

@router.get("/{file_id}/download")
def download_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download a file"""
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    require_file_permission(db, current_user, file, "viewer")

    return FileResponse(
        path=file.file_path,
        filename=file.filename,
        media_type=file.mime_type
    )

@router.delete("/{file_id}")
def delete_file_endpoint(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a file"""
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Only owner can delete
    if file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can delete this file")

    # Delete from disk
    delete_file(file.file_path)

    # Delete from database
    db.delete(file)
    db.commit()

    return {"message": "File deleted successfully"}

@router.get("/")
def list_files(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all files owned by current user"""
    files = db.query(FileModel).filter(FileModel.owner_id == current_user.id).all()
    return files
