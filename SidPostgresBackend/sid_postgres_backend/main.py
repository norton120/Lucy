from typing import Union, TYPE_CHECKING, Optional
from sqlalchemy import create_engine

if TYPE_CHECKING:
    from sqlalchemy import URL

class SidPostgresBackend:
    """adapts sid to use a postgres db
    """

    def __init__(self,
                 connection: Union[str, URL],
                 connect_args: Optional[dict] = None):
        self.engine = create_engine(connection, connect_args=connect_args)

        # initialize adapter
        # migrations
        # init connection pool

    # instance state w/core memory

    # recall memory

    # archival memory
