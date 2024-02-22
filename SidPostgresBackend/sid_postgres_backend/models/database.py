from uuid import UUID
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column


from sid_postgres_backend.models.base import SqlalchemyBase
from sid_postgres_backend.models.mixins import SidAgentInstanceMixin

class SidAgentInstance(SqlalchemyBase):
    """The agent instance that contains both configuration and CORE memory state."""
    __tablename__ = 'sid_agent_instance'
    prefix = "s"
    human: Mapped[str] = mapped_column(Text)

class SidRecallMemory(SqlalchemyBase, SidAgentInstanceMixin):
    """a memory bank for an agent instance, contains the conversation history and the agent's internal monologue."""
    __tablename__ = 'sid_recall_memory'
    prefix = "r"

class SidArchivalMemory(SqlalchemyBase, SidAgentInstanceMixin):
    """a memory bank for an agent instance, contains long-term memory."""
    __tablename__ = 'sid_archival_memory'
    prefix = "a"