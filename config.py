from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    API_KEY: str

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()
