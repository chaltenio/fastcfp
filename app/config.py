from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Fast CFP"
    ADMIN_EMAIL: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file= ".env"

settings = Settings()