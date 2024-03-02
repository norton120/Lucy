from typing import Any, Union, TYPE_CHECKING, Optional
import logging
from sqlalchemy import create_engine

from lucy_postgres_backend.models.base import SqlalchemyBase
from lucy_postgres_backend.exceptions import InstanceNotFound
from lucy_postgres_backend.models.database import LucyAgentInstance

if TYPE_CHECKING:
    from sqlalchemy import URL


logger = logging.getLogger("lucy.postgres_backend")

class LucyPostgresBackend:
    """adapts lucy to use a postgres db
    Init requires an existing agent instance; if one does not exist
    must use the instance bootstrap to create one.
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
                self.db_instance = LucyAgentInstance.read(session, self.instance_id)
            except InstanceNotFound as e:
                logger.error("Unable to find an existing agent instance with id %s", self.instance_id)
                raise e

    def session(self):
        yield self.engine.connect()

    @property
    def core_memory(self) -> "LucyAgentInstance":
        # should assemble current state from instance
        # plus any archival and recall memory requested
        with self.backend.session() as session:
           agent = LucyAgentInstance.read_or_create(session, self.instance_id)

        #TODO: this should be prompt assembly based on an agent prompt template
        return "\n".join([agent.system_message, agent.human, agent.persona])
