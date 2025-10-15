import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@db:5432/app_db")
    """
    JWT 안쓸 것 같아 일단 주석 처리하고 추후 확정 시 삭제
    """
    # SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-prod")
    # ALGORITHM: str = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

settings = Settings()
