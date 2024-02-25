from typing import Optional
from abc import ABC, abstractmethod

from sid.schema import Message

class SidStimuliBase(ABC):
    """All Stimuli must implement this interface.
    """

    @abstractmethod
    def enque(self, message:Message, priority:Optional[bool]=True) -> None:
        """Add this new stimuli to the stimuli queue.
        """
        raise NotImplementedError

    @abstractmethod
    def deque(self) -> Optional[Message]:
        """get the next available stimuli (if any exist) from the stimuli queue.
        Returns None if no stimuli are available.
        """
        raise NotImplementedError