
class Agent:
    """The abstraction that uses different memory banks and an LLM to "think" and "act" in the environment
    """
    def __init__(self,
                  ):
        # for now memories will be configured globally
        # LLMs will also be configured globally
        #

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

