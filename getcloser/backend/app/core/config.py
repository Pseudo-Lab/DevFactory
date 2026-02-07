import os
from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@db:5432/app_db")
    
    """
    JWT 안쓸 것 같아 일단 주석 처리하고 추후 확정 시 삭제
    """
    # Secret key for JWT signing. Must be overridden in production using environment variables.
    DEFAULT_SECRET_KEY = "default-secret-key-change-it"
    SECRET_KEY: str = os.getenv("SECRET_KEY", DEFAULT_SECRET_KEY)
    
    @field_validator("SECRET_KEY")
    @classmethod
    def check_secret_key(cls, v, info):
        """
        Validate that SECRET_KEY is not using the default placeholder value in production.
        """
        env = os.getenv("ENVIRONMENT", "dev").lower()
        if env in ["prod", "production"] and v == cls.DEFAULT_SECRET_KEY:
            raise ValueError("SECRET_KEY must be a unique, non-default value in production environments.")
        return v
        
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

settings = Settings()
