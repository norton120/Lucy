from typing import Optional
from uuid import UUID
from sqlalchemy import Text, String, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column


from sid_postgres_backend.enums import Role
from sid_postgres_backend.models.base import SqlalchemyBase
from sid_postgres_backend.models.mixins import SidAgentInstanceMixin

class AgentInstance(SqlalchemyBase):
    """The agent instance that contains both configuration and CORE memory state."""
    __tablename__ = 'sid_agent_instance'
    prefix = "s"
    human: Mapped[str] = mapped_column(Text, max_length=1000)
    persona: Mapped[str] = mapped_column(Text, max_length=1000)
    system_message: Mapped[str] = mapped_column(Text, max_length=1000)

class RecallMemory(SqlalchemyBase, SidAgentInstanceMixin):
    """contains the conversation history including the agent's internal monologue."""
    __tablename__ = 'sid_recall_memory'
    prefix = "r"
    role: Mapped[Role] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text, max_length=1000)
    tool_call_id: Mapped[Optional[UUID]] = mapped_column(SQLUUID, nullable=True)

class ArchivalMemory(SqlalchemyBase, SidAgentInstanceMixin):
    """a memory bank for an agent instance, contains items Sid has chosen to save."""
    __tablename__ = 'sid_archival_memory'
    prefix = "a"
    thought: Mapped[str] = mapped_column(Text, max_length=1000)
    # TODO: add embeddings