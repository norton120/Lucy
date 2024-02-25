from typing import List, Union, Callable
from abc import ABC, abstractmethod

from sid67.schema import MemoryType, SidMemoryCore, RecallSearchResult, ArchivalSearchResult, Message, Document

class SidMemoryBackendBase(ABC):
    """All memory backends must implement this interface.

    Args:
        instance_id: the unique identifier for the agent instance
        memory_type: the type of memory to be used
    """
    instance_id: str
    memory_type: MemoryType

    def __init__(self,
                 instance_id: str,
                 memory_type: MemoryType):
        self.instance_id = instance_id
        self.memory_type = memory_type

    @classmethod
    @abstractmethod
    def initialize(cls, memory_type: MemoryType):
        """Initializes the memory backend - ie creates initial tables, documents etc.
        Must be idempotent and non-destructive.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def core(self) -> "SidMemoryCore":
        """Returns the persisted (memory state) core IF this is a core memory backend."""
        raise NotImplementedError

    @core.setter
    @abstractmethod
    def core(self, value: "SidMemoryCore"):
        """Sets the persisted (memory state) core IF this is a core memory backend."""
        raise NotImplementedError

    @abstractmethod
    def factory(cls, *args, **kwargs) -> Callable:
        """Override this factory so that a global callable can be used to set up db connections, initialize documents etc.

        NOTE: this must return a callable with the signature (instance_id: str, memory_type: MemoryType) -> SidMemoryBackendBase!
        """
        raise NotImplementedError

    def write(self, items: List[Union[Message, Document]]) -> None:
        """Writes a list of messages to the correct memory."""
        match self.memory_type:
            case MemoryType.core:
                raise ValueError("Core memory must be written to directly as a SidCoreMemory object!")
            case MemoryType.recall:
                self._write_to_recall(items)
            case MemoryType.archival:
                self._write_to_archival(items)
            case _:
                raise ValueError(f"unknown memory type {self.memory_type}, unable to write to it")

    def search(self, value: str, page: int = 1) -> Union[RecallSearchResult, ArchivalSearchResult]:
        """Searches the correct memory for a value."""
        match self.memory_type:
            case MemoryType.core:
                raise ValueError("cannot search core memory, you already have it!")
            case MemoryType.recall:
                return self._search_recall(value, page)
            case MemoryType.archival:
                return self._search_archival(value, page)
            case _:
                raise ValueError(f"unknown memory type {self.memory_type}, unable to search it")

    # search recall
    def _search_recall(self, value: str, page: int = 1) -> RecallSearchResult:
        """Searches the recall memory for a value."""
        raise NotImplementedError

    def _write_to_recall(self, messages: List[Message]) -> None:
        """Commits a list of messages to recall memory."""
        raise NotImplementedError

    # search archival
    def _search_archival(self, value: str, page: int = 1) -> ArchivalSearchResult:
        """Searches the archival memory for a value."""
        raise NotImplementedError

    # write to archival
    def _write_to_archival(self, documents: List[Document]) -> None:
        """Commits a document to archival memory."""
        raise NotImplementedError
