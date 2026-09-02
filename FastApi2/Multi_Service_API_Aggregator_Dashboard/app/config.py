from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openweather_api_key: str
    news_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()