from fastapi import HTTPException, UploadFile
from app.config import settings

def validate_file_size(file: UploadFile, max_mb: int = None):
    """Validate file size doesn't exceed maximum"""
    if max_mb is None:
        max_mb = settings.max_file_size_mb

    max_bytes = max_mb * 1024 * 1024

    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning

    if file_size > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File size ({file_size / 1024 / 1024:.2f}MB) exceeds maximum allowed size ({max_mb}MB)"
        )

    return file_size

def validate_file_extension(filename: str, allowed_extensions: list = None):
    """Validate file extension is allowed"""
    if allowed_extensions is None:
        allowed_extensions = settings.allowed_extensions.split(',')

    file_ext = filename.split('.')[-1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type '.{file_ext}' not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )

    return file_ext
