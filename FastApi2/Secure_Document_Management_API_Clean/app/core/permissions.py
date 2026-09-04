from sqlalchemy.orm import Session
from app.models.permission import Permission, RoleEnum
from app.models.file import File
from app.models.user import User
from fastapi import HTTPException

ROLE_HIERARCHY = {
    "owner": 3,
    "editor": 2,
    "viewer": 1
}

def check_file_permission(db: Session, user: User, file: File, required_role: str) -> bool:
    """
    Check if user has the required permission level for a file
    Returns True if user has permission, False otherwise
    """
    # Owner always has full access
    if file.owner_id == user.id:
        return True

    # Check if user has explicit permission
    permission = db.query(Permission).filter(
        Permission.file_id == file.id,
        Permission.user_id == user.id
    ).first()

    if not permission:
        return False

    # Check role hierarchy
    user_role_level = ROLE_HIERARCHY.get(permission.role.value, 0)
    required_role_level = ROLE_HIERARCHY.get(required_role, 0)

    return user_role_level >= required_role_level

def require_file_permission(db: Session, user: User, file: File, required_role: str):
    """
    Check file permission and raise HTTPException if denied
    """
    if not check_file_permission(db, user, file, required_role):
        raise HTTPException(
            status_code=403,
            detail=f"Permission denied. Required role: {required_role}"
        )
