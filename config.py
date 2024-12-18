from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    API_KEY: str
    
    model_config = ConfigDict(extra="allow", env_file=".env")


def get_settings():
    return Settings()
