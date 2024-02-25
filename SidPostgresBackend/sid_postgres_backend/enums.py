from enum import Enum

class Role(str, Enum):
    """The role of a message in a conversation."""
    assistant = "assistant"
    tool = "tool"
    system = "system"
    user = "user"