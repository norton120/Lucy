from typing import Optional
from uuid import uuid4

from sid_postgres_backend import ScopedMemory

from sid.settings import settings
from sid.freud_id.agent.perpetuation import Perpetulation
from sid.message_queues.cli_queue import CLIQueue

class Agent:
    """The abstraction that uses different memory banks and an LLM to "think" and "act" in the environment
    """
    perpetulation: "Perpetulation"
    message_queue: "CLIQueue"
    core_memory: "ScopedMemory"
    archival_memory: "ScopedMemory"
    recall_memory: "ScopedMemory"

    def __init__(self,
                 instance_id: Optional[str] = None,
                  ):
        self.instance_id = instance_id or f"s_{str(uuid4())}"
        self.perpetulation = Perpetulation(self)
        self.message_queue = CLIQueue()
        for memory_type in ("archival","core", "recall",):
            setattr(self, f"{memory_type}_memory", getattr(settings, f"{memory_type}_backend").get_scoped_memory(self.instance_id))
        # do we configure LLMs and Memory providers here?
        # what about the memory state instance - what exactly is that?
        # you've got:
        # an identifier to map:
            # each memory type to the correct agent instance
            # the comms channel to message the user
            # the comms channel to receiving messages from the user
            # ... I think that's it?

    # assemble the core memory - system prompt plus (summarized) messages + available functions

    # manipulate messages history
        # -
    # request generations to LLM

    # process responses from LLM
        # save internal monologue to memory
        # execute tool calls
            # write call errors to messages and heartbeat to make it deal with it
        # send messages to user
        # save messages to memory

    # Heartbeat:
        # resize the memory contents based on memory pressure

    # summarize messages in place

