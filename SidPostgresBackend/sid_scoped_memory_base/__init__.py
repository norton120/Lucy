from typing import Optional
from abc import ABC, abstractmethod

from sid_scoped_memory_base.schema import SidAgentInstance

class SidScopedMemoryBase(ABC):
    """The standard interface required for all Sid memory backends"""

    @abstractmethod
    def core_memory(self, instance_id: Optional[str]=None) -> SidAgentInstance:
        """The core memory of the agent instance"""
        raise NotImplementedError
