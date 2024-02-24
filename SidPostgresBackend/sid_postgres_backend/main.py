from typing import Any, Union, TYPE_CHECKING, Optional
import logging
from sqlalchemy import create_engine


from sid_scoped_memory_base import SidScopedMemoryBase

from sid_postgres_backend.models.base import SqlalchemyBase
from sid_postgres_backend.exceptions import InstanceNotFound
from sid_postgres_backend.models.database import SidAgentInstance

if TYPE_CHECKING:
    from sqlalchemy import URL


logger = logging.getLogger("sid.postgres_backend")

class SidPostgresBackend:
    """adapts sid to use a postgres db
    """
    instance_id: str

    def __init__(self,
                 instance_id: str,
                 connection: Union[str, URL],
                 connect_args: Optional[dict] = None):

        self.instance_id = instance_id
        self.engine = create_engine(connection, connect_args=connect_args)

        # TODO: integrate with migrations
        SqlalchemyBase.metadata.create_all(self.engine)

        with self.session() as session:
            # TODO need base settings for prompts
            try:
                self.db_instance = SidAgentInstance.read(session, self.instance_id)
            except InstanceNotFound as e:
                logger.error("Unable to find an existing agent instance with id %s", self.instance_id)
                raise e


    def session(self):
        yield self.engine.connect()

    @property
    def core_memory(self) -> "SidAgentInstance":
        # should assemble current state from instance
        # plus any archival and recall memory requested
        with self.backend.session() as session:
           agent = SidAgentInstance.read_or_create(session, self.instance_id)

        #TODO: this should be prompt assembly based on an agent prompt template
        return "\n".join([agent.system_message, agent.human, agent.persona])
