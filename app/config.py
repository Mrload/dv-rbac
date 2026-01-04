from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = ""
    DATABASE_URL: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    SUPER_ADMIN_USERNAME: str = "admin"
    SUPER_ADMIN_PASSWORD: str = "admin"

    class Config:
        env_file = ".env"


settings = Settings()

