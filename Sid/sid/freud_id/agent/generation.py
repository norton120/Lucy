from enum import Enum
from pydantic import BaseModel, Field

class GenerationRole(str, Enum):
    """The role of the generation. This is a simple enum to help with the typing of the generation."""
    ASSISTANT = "assistant"
    USER = "user"
    SYSTEM = "system"

class GenerationToolArgument(BaseModel):
    """a representation of an argument that a tool takes"""
    name: str = Field(description="the name of the argument")
    type: str = Field(description="the type of the argument")
    description: str = Field(description="a description of the argument")
    default: str = Field(description="the default value of the argument")
    required: bool = Field(description="whether the argument is required")

class GenerationTool(BaseModel):
    """a representation of a tool that is available to the LLM to execute"""
    name: str = Field(description="the name of the tool")
    arity: list[GenerationToolArgument] = Field(description="the arguments that the tool takes")
    returns: str = Field(description="the type of the return value of the tool")
    description: str = Field(description="a description of the tool")

class Generation(BaseModel):
    """This is the single construct for a request to be sent to an LLM. It is model/platform/LLM Server agnostic.

    Note: this is going to look tightly coupled to the OpenAI spec; that is because OAI is the default standard in the space.
    under the hood, backends need to convert this structure as needed to support their respective LLMs.

    The grain of a generation is a single message.
    """
    prompt: str = Field(description="the text to be packaged and presented to the LLM")
    role: GenerationRole
    available_tools: list[GenerationTool] = Field(description="the tools that are available to the LLM to execute")
