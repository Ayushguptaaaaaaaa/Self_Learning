import os
import uuid
from fastapi import UploadFile
from app.config import settings

def save_upload_file(file: UploadFile) -> tuple:
    """
    Save uploaded file to disk
    Returns: (stored_filename, file_path, size_bytes, mime_type)
    """
    # Generate unique filename
    file_extension = file.filename.split('.')[-1]
    stored_filename = f"{uuid.uuid4()}.{file_extension}"

    # Create upload directory if it doesn't exist
    os.makedirs(settings.upload_dir, exist_ok=True)

    # Full file path
    file_path = os.path.join(settings.upload_dir, stored_filename)

    # Save file
    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)

    size_bytes = len(content)
    mime_type = file.content_type or "application/octet-stream"

    return stored_filename, file_path, size_bytes, mime_type

def delete_file(file_path: str) -> bool:
    """Delete file from disk"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False
