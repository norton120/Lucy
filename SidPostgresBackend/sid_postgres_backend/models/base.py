from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Boolean, DateTime, func, text, UUID as SQLUUID
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declarative_mixin,
    declared_attr,
)

@declarative_mixin
class SqlalchemyBase(DeclarativeBase):
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
    async def list(cls, db_session: "AsyncSession") -> list["SqlalchemyBase"]:
        """list all the objects in the database."""
        logger.info("listing %s", str(cls))
        query = select(cls).where(cls.is_deleted == False)
        result = await db_session.execute(query)
        all_found = result.scalars().all()
        logger.info("found %s %s", len(all_found), str(cls))
        return all_found

    async def create(
        self, db_session: "AsyncSession", persist: Optional[bool] = True
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
        _ = await db_session.flush()
        if persist:
            _ = await db_session.commit()
        _ = await db_session.refresh(self)
        return self

    @classmethod
    async def read(
        cls, _id: str, db_session: "AsyncSession", show_deleted: bool = False
    ) -> "SqlalchemyBase":
        """Read an object from the database.
        Args:
            - A database session.
            - show_deleted: If True, return deleted objects too.
        Returns: The object.
        Raises: InstanceNotFound if the object is not found.
        Example:
            user = User.read("usr_1234", db_session)
        """
        logger.info("reading %s %s", str(cls), _id)
        prefix, id_ = _id.split("_")
        assert (
            prefix == cls.prefix
        ), f"{prefix} is not a valid id prefix for {cls.__name__}"
        query = select(cls).where(cls._id == UUID(id_))
        if not show_deleted:
            query = query.where(cls.is_deleted == False)
        result = await db_session.execute(query)
        found = result.unique().scalar_one_or_none()
        if not found:
            logger.error("no %s found for read lookup", cls.__name__)
            raise InstanceNotFound(f"{cls.__name__} not found for id {_id}")
        logger.info("found %s for read lookup", found)
        return found

    async def update(
        self, db_session: "AsyncSession", persist: Optional[bool] = True
    ) -> "SqlalchemyBase":
        """Update this object in the database.
        Args:
            persist: should the update be committed? usefull for external transactions
        Note: this logically could just be skipped with "persist" set to false, but
        calling the verb makes for very readable code in many cases.
        Returns: The object.
        Example:
            user = User.read("usr_1234", db_session)
            user.username = "bar"
            user.update(db_session)
        """
        logger.info("updating %s %s", str(self.__class__), self.id)
        _ = await db_session.flush()
        if persist:
            _ = await db_session.commit()
        _ = await db_session.refresh(self)
        return self

    async def delete(
        self, db_session: "AsyncSession", perist: Optional[bool] = True
    ) -> None:
        """Soft deletes the object from the database.
        Args:
            persist: should the delete be committed?
        """
        logger.info("(soft) deleting %s %s", str(self.__class__), self.id)
        self.is_deleted = True
        _ = await db_session.flush()
        if perist:
            _ = await db_session.commit()
