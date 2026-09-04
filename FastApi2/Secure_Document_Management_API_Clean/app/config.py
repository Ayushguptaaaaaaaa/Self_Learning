from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str

    # JWT Configuration
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    # File Upload Configuration
    max_file_size_mb: int
    upload_dir: str
    allowed_extensions: str

    # Storage Quota
    user_storage_quota: int

    class Config:
        env_file = ".env"

settings = Settings()