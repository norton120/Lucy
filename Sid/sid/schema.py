from datetime import datetime
from typing import Optional, Literal, List
from enum import Enum
from pydantic import BaseModel, Field, model_validator

"""The Sid Schema acts as a canonical representation of the data for all things in Sid."""

class Role(str, Enum):
    """The role of a message in a conversation."""
    assistant = "assistant"
    tool = "tool"
    system = "system"
    user = "user"


class SidSchema(BaseModel):
    """All first-class objects in Sid are defined as children of SidSchema.
    When different plugins and backends interact they must exchange SidSchema objects (no localized db or platform specific objects).
    """

### GENERATION ###

class ToolCallFunction(SidSchema):
    """represents a function request for execution by the model."""
    name: str = Field(description="the name of the function to be executed")
    arguments: dict = Field(description="the arguments to be passed to the function", default_factory=lambda: {})

class ToolCall(SidSchema):
    """represents a request by the model to execute a tool."""
    id: str = Field(description="the unique identifier for the request to execute this tool")
    type: Literal["function"] = Field(description="the type of the tool to be executed, always function at the moment", default = "function")
    function: ToolCallFunction = Field(description="the function to be executed")

class Message(SidSchema):
    """The canonical packet containing text - often (incorrectly) referred to as a prompt.
    The message object is bidirectional - the LLM receives a message and returns a message.
    Messages belong to a speaker (identified by "role"), and contain at minium content (the text of the message).
    May also contain tool_calls (see above).
    """
    timestamp: Optional[float] = Field(description="the time the message was sent/recorded/created", default_factory= lambda : datetime.now().timestamp())
    role: Role
    content: str = Field(description="the text body of the message")
    tool_calls: Optional[list[ToolCall]] = Field(description="a list of tool calls requested to be executed", default = None)
    tool_call_id: Optional[str] = Field(description="the id of the tool call that was executed", default = None)

    @model_validator(model="before")
    @classmethod
    def valid_tool_message(cls, values):
        if values["role"] == "tool":
            if values["tool_call_id"] is None:
                raise ValueError("Messages from tools must contain a tool call id")
        return values

class ToolParameter(SidSchema):
    """representation of a parameter that a tool takes."""
    name: str = Field(description="the name of the parameter")
    type: str = Field(description="the type of the parameter")
    description: str = Field(description="a description of the parameter")
    default: str = Field(description="the default value of the parameter")
    required: bool = Field(description="whether the parameter is required")
    enum: Optional[list[str]] = Field(description="the possible values of the parameter", default = None)

class Tool(SidSchema):
    """representation of a function made available to the LLM to execute."""
    type: Literal["function"] = Field(description="the type of the tool, always function at the moment", default = "function")
    description: str = Field(description="a description of the tool")
    name: str = Field(description="the name of the tool", patter=r"^[a-zA-Z0-9_-]{1,64}$")
    parameters: Optional[list[ToolParameter]] = Field(description="the parameters that the tool takes", default= None)

class Turn(SidSchema):
    """Much like a board game, a 'turn' in Sid represents one complete pass through the model.
    A turn consists of the payload sent to the LLM and the response from the LLM.
    Things can and will happen inbetween turns; for example, the output of a turn can be a function call. The execution of that call and the resulting output will not be captured in the turn
    (but will be added to the input at the beginning of the next turn).
    """
    request_messages = list[Message]
    request_tools = list[Tool]
    response_message = Optional[Message] = None

### KNOWLEDGE ###

class Document(SidSchema):
    """A document is a piece of knowledge that the LLM can use to generate responses."""
    content: str = Field(description="the text of the document")
    embeddings: list[float] = Field(description="the embeddings of the document")


### MEMORY ###

class MemoryType(str, Enum):
    """The type of memory."""
    core = "core"
    archival = "archival"
    recall = "recall"

class SidMemoryCore(SidSchema):
    """The core memory components of an agent."""
    boot: str = Field(description="the system 'boot' message section of core memory, which introduces the LLM to the new agent instance")
    bios: str = Field(description="the system 'bios' message section of core memory, which details how core memory is to be used to the LLM")
    persona: str = Field(description="the persona section of core memory, describing the agent's personality")
    human: str = Field(description="the human section of core memory, describing the user")
    history: list[Message] = Field(description="the visible message history for the agent")

    def fifo_history(self, message: Message, max_length: int = 100) -> List[Optional[Message]]:
        """Adds a message to the history, removing the oldest message if the history is at the maximum length."""
        self.history.append(message)
        removed = []
        while len(self.history) > max_length:
            removed.append(self.history.pop(0))
        return removed

class RecallSearchResult(SidSchema):
    """A resultset from a recall memory search."""
    results: list[Message] = Field(description="the messages that matched the search criteria")
    page: int = Field(description="the page number of these results")
    page_count: int = Field(description="the total number of pages of results")
    query: str = Field(description="the query that was used to search")

class ArchivalSearchResult(SidSchema):
    """A resultset from a Archival memory search."""
    results: list[Document] = Field(description="the documents found in the search")
    page: int = Field(description="the page number of these results")
    page_count: int = Field(description="the total number of pages of results")
    query: str = Field(description="the query that was used to search")