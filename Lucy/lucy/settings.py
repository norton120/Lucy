from typing import Any
from pydantic_settings import BaseSettings

from lucy_postgres_backend import LucyPostgresBackend

memory_backend = LucyPostgresBackend("postgresql://lucy:lucy@localhost/lucy")

class Settings(BaseSettings):
    core_backend: Any = memory_backend
    archive_backend: Any = memory_backend
    recall_backend: Any = memory_backend


# singleton pattern
settings = Settings()