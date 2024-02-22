from typing import Optional
from uuid import UUID
from sqlalchemy import UUID as SQLUUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from sid_postgres_backend.models.base import SqlalchemyBase

class MalformedIdError(Exception):
    pass

def _relation_getter(instance: "SqlalchemyBase", prop: str, prefix: str) -> Optional[str]:
    if not getattr(instance, prop):
        return None
    formatted_prop = f"_{prop}_id"
    uuid_ = getattr(instance, formatted_prop)
    return f"{prefix}_{uuid_}"


def _relation_setter(instance: "SqlalchemyBase", prop: str, prefix: str, value: str) -> None:
    formatted_prop = f"_{prop}_id"
    if not value:
        setattr(instance, formatted_prop, None)
        return
    try:
        found_prefix, id_ = value.split("_")
    except ValueError as e:
        raise MalformedIdError(f"{value} is not a valid ID.") from e
    assert (
        found_prefix
        == prefix
    ), f"{found_prefix} is not a valid id prefix, expecting {prefix}"
    try:
        setattr(instance, formatted_prop, UUID(id_))
    except ValueError as e:
        raise MalformedIdError("Hash segment of {value} is not a valid UUID") from e


class SidAgentInstanceMixin(SqlalchemyBase):
    """Mixin for models that belong to an agent instance."""

    __abstract__ = True

    _agent_instance_id: Mapped[UUID] = mapped_column(
        SQLUUID(), ForeignKey("sid_agent_instance._id")
    )

    @property
    def agent_instance_id(self) -> str:
        return _relation_getter(self, "sid_agent_instance", "s")

    @agent_instance_id.setter
    def agent_instance_id(self, value: str) -> None:
        return _relation_setter(self, "sid_agent_instance", "s", value)