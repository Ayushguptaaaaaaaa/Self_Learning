from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.folder import Folder
from app.models.file import File
from app.schemas.folder import FolderCreate, FolderResponse, FolderUpdate

router = APIRouter(prefix="/api/folders", tags=["Folders"])

@router.post("/", response_model=FolderResponse)
def create_folder(
    folder_data: FolderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new folder"""
    new_folder = Folder(
        name=folder_data.name,
        owner_id=current_user.id,
        parent_id=folder_data.parent_id
    )
    db.add(new_folder)
    db.commit()
    db.refresh(new_folder)

    return new_folder

@router.get("/{folder_id}", response_model=FolderResponse)
def get_folder(
    folder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get folder details and list contents"""
    folder = db.query(Folder).filter(Folder.id == folder_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    if folder.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return folder

@router.get("/{folder_id}/contents")
def list_folder_contents(
    folder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all files and subfolders in a folder"""
    folder = db.query(Folder).filter(Folder.id == folder_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    if folder.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Get subfolders
    subfolders = db.query(Folder).filter(Folder.parent_id == folder_id).all()

    # Get files
    files = db.query(File).filter(File.folder_id == folder_id).all()

    return {
        "folder": folder,
        "subfolders": subfolders,
        "files": files
    }

@router.put("/{folder_id}", response_model=FolderResponse)
def rename_folder(
    folder_id: int,
    folder_data: FolderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Rename a folder"""
    folder = db.query(Folder).filter(Folder.id == folder_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    if folder.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can rename this folder")

    folder.name = folder_data.name
    db.commit()
    db.refresh(folder)

    return folder

@router.delete("/{folder_id}")
def delete_folder(
    folder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a folder and all its contents"""
    folder = db.query(Folder).filter(Folder.id == folder_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    if folder.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can delete this folder")

    # Delete all files in folder
    files = db.query(File).filter(File.folder_id == folder_id).all()
    for file in files:
        from app.utils.file_handler import delete_file
        delete_file(file.file_path)
        db.delete(file)

    # Delete folder
    db.delete(folder)
    db.commit()

    return {"message": "Folder deleted successfully"}

@router.get("/")
def list_folders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all root folders owned by current user"""
    folders = db.query(Folder).filter(
        Folder.owner_id == current_user.id,
        Folder.parent_id == None
    ).all()
    return folders
