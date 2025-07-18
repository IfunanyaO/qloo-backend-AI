from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "development"
    OPENAI_API_KEY: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str
    POSTGRES_DB:str
    POSTGRES_HOST:str
    POSTGRES_PORT:str

    class Config:
        env_file = ".env"


settings = Settings()
