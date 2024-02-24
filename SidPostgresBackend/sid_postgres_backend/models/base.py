from typing import Optional, TYPE_CHECKING
import logging
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Boolean, DateTime, func, text, UUID as SQLUUID, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declarative_mixin,
)

logger = logging.getLogger("sid.postgres")

from sid_postgres_backend.exceptions import InstanceNotFound

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

class DBBase(DeclarativeBase):
    __abstract__ = True


@declarative_mixin
class SqlalchemyBase(DBBase):
    __abstract__ = True

    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, server_default=text("FALSE"))

    _id: Mapped[UUID] = mapped_column(SQLUUID(), primary_key=True, default=uuid4)

    @property
    def id(self) -> Optional[str]:
        if self._id:
            return f"{self.prefix}_{self._id}"

    @id.setter
    def id(self, value: str) -> None:
        if not value:
            return
        prefix, id_ = value.split("_")
        assert (
            prefix == self.prefix
        ), f"{prefix} is not a valid id prefix for {self.__class__.__name__}"
        self._id = UUID(id_)

    @classmethod
    def list(cls, db_session: "Session") -> list["SqlalchemyBase"]:
        """list all the objects in the database."""
        logger.info("listing %s", str(cls))
        query = select(cls).where(cls.is_deleted == False)
        result = db_session.execute(query)
        all_found = result.scalars().all()
        logger.info("found %s %s", len(all_found), str(cls))
        return all_found

    def create(
        self, db_session: "Session", persist: Optional[bool] = True
    ) -> "SqlalchemyBase":
        """Add this object to the database.
        Args:
            persist: should the create be committed? usefull for external transactions
        Returns: The object.
        Example:
            user = User(username="foo", password="bar").create(db_session)
        """
        if created_by := getattr(self, "created_by", False):
            if not self.last_updated_by_id:
                self.last_updated_by_id = created_by.id
        db_session.add(self)
        _ = db_session.flush()
        if persist:
            _ = db_session.commit()
        _ = db_session.refresh(self)
        return self

    @classmethod
    def read(
        cls, _id: str, db_session: "Session", show_deleted: bool = False
    ) -> "SqlalchemyBase":
        """Read an object from the database.
        Args:
            - A database session.
            - show_deleted: If True, return deleted objects too.
        Returns: The object.
        Raises: InstanceNotFound if the object is not found.
        Example:
            user = SidAgentInstance.read("s_1234", db_session)
        """
        logger.info("reading %s %s", str(cls), _id)
        prefix, id_ = _id.split("_")
        assert (
            prefix == cls.prefix
        ), f"{prefix} is not a valid id prefix for {cls.__name__}"
        query = select(cls).where(cls._id == UUID(id_))
        if not show_deleted:
            query = query.where(cls.is_deleted == False)
        result = db_session.execute(query)
        found = result.unique().scalar_one_or_none()
        if not found:
            logger.error("no %s found for read lookup", cls.__name__)
            raise InstanceNotFound(f"{cls.__name__} not found for id {_id}")
        logger.info("found %s for read lookup", found)
        return found

    def delete(
        self, db_session: "Session", perist: Optional[bool] = True
    ) -> None:
        """Soft deletes the object from the database.
        Args:
            persist: should the delete be committed?
        """
        logger.info("(soft) deleting %s %s", str(self.__class__), self.id)
        self.is_deleted = True
        _ = db_session.flush()
        if perist:
            _ = db_session.commit()

    def read_or_create(self, db_session:"Session"):
        try:
            return self.read(self.id, db_session)
        except InstanceNotFound:
            return self.create(db_session)