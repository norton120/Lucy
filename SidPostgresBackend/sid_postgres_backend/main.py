from typing import Any, Union, TYPE_CHECKING, Optional
from sqlalchemy import create_engine


from sid_postgres_backend.models.base import SqlalchemyBase
from sid_postgres_backend.exceptions import InstanceNotFound
from sid_postgres_backend.models.database import SidAgentInstance

if TYPE_CHECKING:
    from sqlalchemy import URL

class SidPostgresBackend:
    """adapts sid to use a postgres db
    """

    def __init__(self,
                 connection: Union[str, URL],
                 connect_args: Optional[dict] = None):
        self.engine = create_engine(connection, connect_args=connect_args)

        # TODO: integrate with migrations
        SqlalchemyBase.metadata.create_all(self.engine)

    def get_scoped_memory(self, instance_id: str) -> "ScopedMemory":
        return ScopedMemory(instance_id, self)

    def session(self):
        yield self.engine.connect()


class ScopedMemory:
    """A memory bank scoped to a specific agent"""
    instance_id: str
    backend: "SidPostgresBackend"

    def __call__(self,
                 instance_id:str,
                 backend:"SidPostgresBackend") -> Any:
        self.instance_id = instance_id
        self.backend = backend

    @property
    def core_memory(self) -> str:
        # should assemble current state from instance
        # plus any archival and recall memory requested
        with self.backend.session() as session:
           agent = SidAgentInstance.read_or_create(session, self.instance_id)

        #TODO: this should be prompt assembly based on an agent prompt template
        return "\n".join([agent.system_message, agent.human, agent.persona])
