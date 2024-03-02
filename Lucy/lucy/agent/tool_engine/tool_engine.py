from typing import List
from lucy.schema import ToolCall, Message, Tool


class ToolEngine:
    """Manages the tool ecosystem. Responsible for discovering valid tools,
    presenting them to the inference backend,
    executing tool calls,
    feeding the results back as stimuli,
    and conducting searches for tools when too many are availabe to list at once.


    This needs to build a stack of tools with a heirarchy:
    1. user-defined
    2. backend-defined
    3. os defined

    if the stack gets too large (inference backend setting?) it needs to add functionality to search tools and add those to the following Turn.
    """


    def execute(self, tool_call:ToolCall) -> Message:
        """Executes the tool call and returns the result.
        """
        try:
            # look up, parse, and execute the tool here
            pass
        except Exception as e:
            # construct a tools message with the error
            # also warn the shit out of someone - this could turn into a broken loop otherwise
            pass

    @property
    def os_tools(self) -> List[Tool]:
        """get only the tools that are used by the Lucy 'Operating System' - including all those offered by the inference and different memory backends"""
        raise NotImplementedError