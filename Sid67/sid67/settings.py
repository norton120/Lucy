from typing import Any
from pydantic_settings import BaseSettings

from sid_postgres_backend import SidPostgresBackend

memory_backend = SidPostgresBackend("postgresql://sid:sid@localhost/sid")

class Settings(BaseSettings):
    core_backend: Any = memory_backend
    archive_backend: Any = memory_backend
    recall_backend: Any = memory_backend


# singleton pattern
settings = Settings()