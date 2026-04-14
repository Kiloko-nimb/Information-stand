from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./kkrit.db"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"

    # App
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()
