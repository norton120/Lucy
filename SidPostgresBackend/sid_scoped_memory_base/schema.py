from typing import Optional
from pydantic import BaseModel


class CoreMemory(BaseModel):
    """The components that make up an Agent's current context window in full."""
    human: str
    persona: str
    system: str
    archive: Optional[str]
    recall: Optional[str]