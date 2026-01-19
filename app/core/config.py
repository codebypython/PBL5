"""
Application configuration using Pydantic Settings.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = "OldGoods Marketplace"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DB_USER: str = "oldgoods_user"
    DB_PASSWORD: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "oldgoods_db"
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL."""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Security
    SECRET_KEY: str = "change-this-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Redis (for WebSocket)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    USE_REDIS: bool = False
    
    # File Storage
    MEDIA_ROOT: str = "media"
    STATIC_ROOT: str = "static"
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    
    # Email (Optional)
    EMAIL_HOST: str = ""
    EMAIL_PORT: int = 587
    EMAIL_USE_TLS: bool = True
    EMAIL_HOST_USER: str = ""
    EMAIL_HOST_PASSWORD: str = ""
    DEFAULT_FROM_EMAIL: str = "noreply@oldgoods.example.com"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
