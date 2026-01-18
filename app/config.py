from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    MONGODB_URI: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7
    DATABASE_URL: str
    cloudinary_cloud_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()
