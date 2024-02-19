from sid.freud_id.agent.perpetuation import Perpetulation
from sid.message_queues.cli_queue import CLIQueue

class Agent:
    """The abstraction that uses different memory banks and an LLM to "think" and "act" in the environment
    """
    def __init__(self,
                  ):
        self.perpetulation = Perpetulation(self)
        self.message_queue = CLIQueue()

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

