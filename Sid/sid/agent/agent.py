from typing import Optional, TYPE_CHECKING
from datetime import datetime
import logging

from sid.settings import settings
from sid.schema import SidMemoryCore, Role
from sid.agent.prompt_engine import PromptEngine
from sid.agent.tool_engine import ToolEngine

if TYPE_CHECKING:
    from sid.backends.inference_backend_base import SidInferenceBackendBase
    from sid.backends.memory_backend_base import SidMemoryBackendBase
    from sid.stimuli.stimuli_base import SidStimuliBase
    from sid.schema import Message

# TODO: real library logging https://docs.python.org/3/howto/logging-cookbook.html#adding-handlers-other-than-nullhandler-to-a-logger-in-a-library
logger = logging.getLogger("sid.agent")

class Agent:
    """The abstraction that uses different memory banks and an LLM to "think" and "act"

    inference_backend is the backend that the agent uses to assemble core memory and generate responses.
    core memory is an in-memory object of the current context window.
    persisted_core_memory, archival_memory, and recall_memory are the backends the agent can access to store and retrieve information.
    stimuli_queue is the inbound information to be added to core memory, in the form of Messages.
    heartrate is the frequency at which the agent should 'think'
    heartbeat is the next time the agent will 'think'

    """
    prompt_engine: "PromptEngine"
    tool_engine: "ToolEngine"
    inference_backend: "SidInferenceBackendBase"
    stimuli_queue: "SidStimuliBase"
    core_memory: "SidMemoryCore"
    persisted_core_memory: "SidMemoryBackendBase"
    archival_memory: "SidMemoryBackendBase"
    recall_memory: "SidMemoryBackendBase"
    heartbeat: float

    def __init__(self,
                 instance_id: Optional[str] = None,
                 inference_backend: Optional["SidInferenceBackendBase"] = None,
                 stimuli_queue: Optional["SidStimuliBase"] = None,
                 core_memory_backend: Optional["SidMemoryBackendBase"] = None,
                 archival_memory_backend: Optional["SidMemoryBackendBase"] = None,
                 recall_memory_backend: Optional["SidMemoryBackendBase"] = None,
                 heartrate: Optional[int] = 60,
                 alternate_tools_path: Optional[str] = None,
                  ):
        """Initializes the agent instance and launches the daemon.
        Args:
            instance_id: the unique identifier for the agent instance
            heartrate: the frequency at which the agent should 'think'
        """
        self.inference_backend = inference_backend or settings.inference_backend
        self.stimuli_queue = stimuli_queue or settings.stimuli_queue
        self.heartrate = heartrate
        self.prompt_engine = PromptEngine(*self.inference_backend.prompt_engine_args)
        self.tool_engine = ToolEngine(alternate_tools_path)

        for backend in (("persisted_core_memory_backend", core_memory_backend),
                        ("archival_memory_backend", archival_memory_backend),
                        ("recall_memory_backend", recall_memory_backend)):
            memory_type = backend[0].split("_")[-3]
            initialized = backend[1](instance_id=instance_id, memory_type=memory_type)
            setattr(self, backend[0], initialized)


        self.core_memory = SidMemoryCore(
            boot=self.prompt_engine.render("boot"),
            human=self.prompt_engine.render("human"),
            persona=self.prompt_engine.render("persona")
        )

        if instance_id:
            self.instance_id = instance_id
            self.core_memory = self.persisted_core_memory.core

        # start the daemon
        self.daemon()


    def daemon(self):
        """the 'cognitive loop' of our agent. Continually processes existing 'thoughts', new stimuli, and generating responses."""

        while "Continue thinking":

            if datetime.now().timestamp() <= self.heartbeat:
                continue

            # for now, don't guard the daemon. Let's get to a point where the think loop is pretty well hardened and then worry about it
            if new_thought := self.stimuli_queue.deque():
                self.adust_recall_memory(new_thought)
            self.think()
            self.heartbeat = datetime.now().timestamp() + self.heartrate


    def think(self):
        """The process of incorporating stimuli into core memory, generating with that memory, and executing any tool calls in the response."""
        response_message = self.inference_backend.generate(self.core_memory)

        self.adust_recall_memory(response_message)

        # intentionally blocking
        if response_message.request_tools:
            for tool_call in response_message.request_tools:
                # some kind of tool handler that merges internal tools with a tools folder in the downstream project
                tool_response:Message = self.tool_engine.execute(tool_call)
                self.stimuli_queue.append(tool_response)
            self.heartbeat = 0 # always force an immediate generation after tool calls


    def core_memory_check(self) -> None:
        """check the state of core memory, and if it needs to be resized, add a stimuli to do so."""

        for segment in ("persona", "human",):
            max_chars = getattr(self.inference_backend, f"core_memory_maximum_chars_in_{segment}")
            if len(getattr(self.core_memory, segment)) > max_chars:

                self.stimuli_queue.enque(
                    self.os_message(
                        self.prompt_engine.render("core_memory_resize",
                                                  segment=segment,
                                                  max_chars=max_chars)
                    ),
                    priority=True
                )

    def adust_recall_memory(self, new_thought: "Message"):
        """check the number of recall memory entries in core, and adjust them if necessary."""
        logger.debug("Inserting new thought into core memory....")
        if redacted := self.core_memory.fifo_history(new_thought, self.inference_backend.core_memory_maximum_number_of_messages_in_history):
            logger.debug(f"Inserted new thought. Redacted {len(redacted)} messages from core memory history, pushing them to recall memory.")
            self.recall_memory.write(redacted)
            logger.debug("Redacted messages pushed to recall memory.")
            return
        logger.debug("Inserted new thought. No redaction necessary.")


    def os_message(self, content: str):
        """construct an 'operating system' message to be added to the stimuli queue.

        These are messages that inform the LLM an internal action must be taken, such as resizing memory.
        """
        return Message(
            content=content,
            role=Role.system,
            tools=self.tool_engine.os_tools
        )