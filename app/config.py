from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Blog API"
    SECRET_KEY: str = "hfaushbfub4u23b4u32b4b324j3" # default
    ALGORITHM: str = "HS256" # default
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 80
    SQLALCHEMY_DATABASE_URL: str = "postgresql://admin:admin@db/app" # default

    class Config:
        case_sensitive = True
        env_prefix = ''
        env_file = '../.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    return Settings(_env_file='.env', _env_file_encoding='utf-8')
