from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    together_ai_key: str

# singleton pattern
settings = Settings()