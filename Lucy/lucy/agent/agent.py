from typing import Optional, TYPE_CHECKING, List
from datetime import datetime
import logging

from threading import Thread

from lucy.settings import settings
from lucy.schema import LucyMemoryCore, Role, ToolCall
from lucy.agent.prompt_engine import PromptEngine
from lucy.agent.tool_engine import ToolEngine

if TYPE_CHECKING:
    from lucy.backends.inference_backend_base import LucyInferenceBackendBase
    from lucy.backends.memory_backend_base import LucyMemoryBackendBase
    from lucy.stimuli.stimuli_base import LucyStimuliBase
    from lucy.schema import Message

# TODO: real library logging https://docs.python.org/3/howto/logging-cookbook.html#adding-handlers-other-than-nullhandler-to-a-logger-in-a-library
logger = logging.getLogger("lucy.agent")

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
    inference_backend: "LucyInferenceBackendBase"
    stimuli_queue: "LucyStimuliBase"
    core_memory: "LucyMemoryCore"
    persisted_core_memory: "LucyMemoryBackendBase"
    archival_memory: "LucyMemoryBackendBase"
    recall_memory: "LucyMemoryBackendBase"
    thinking_heartbeat: float
    os_heartbeat: float

    def __init__(self,
                 instance_id: Optional[str] = None,
                 inference_backend: Optional["LucyInferenceBackendBase"] = None,
                 stimuli_queue: Optional["LucyStimuliBase"] = None,
                 core_memory_backend: Optional["LucyMemoryBackendBase"] = None,
                 archival_memory_backend: Optional["LucyMemoryBackendBase"] = None,
                 recall_memory_backend: Optional["LucyMemoryBackendBase"] = None,
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


        self.core_memory = LucyMemoryCore()

        if instance_id:
            self.instance_id = instance_id
            # load existing core state
            self.core_memory = self.persisted_core_memory.core

        # start the daemons
        #TODO: graceful start/stop control
        #TODO: need observability inside here
        if False:
            Thread(target=self.thinking_daemon).start()
            Thread(target=self.operating_system_daemon).start()
        else:
            # this is just for testing while I'm on the plane
            self.combined_daemon()


    def thinking_daemon(self):
        """the 'cognitive loop' of our agent. Continually processes existing 'thoughts', new stimuli, and generating responses."""

        while "Continue thinking":
            if datetime.now().timestamp() >= self.thinking_heartbeat:
                # for now, don't guard the daemon. Let's get to a point where the think loop is pretty well hardened and then worry about it
                if new_thought := self.stimuli_queue.deque():
                    self.adust_recall_memory(new_thought)
                self.think()
                self.thinking_heartbeat = datetime.now().timestamp() + self.heartrate

    def operating_system_daemon(self):
        """the 'operating system loop' of our agent. Continually processes internal messages, such as resizing memory."""

        while "Continue operating":
            if datetime.now().timestamp() >= self.os_heartbeat:
                self.os_cycle()
                self.os_heartbeat = datetime.now().timestamp() + self.heartrate

    def combined_daemon(self):

        while "Continue thinking and operating":
            if datetime.now().timestamp() >= self.thinking_heartbeat:
                if new_thought := self.stimuli_queue.deque():
                    self.adust_recall_memory(new_thought)
                self.think()
                self.thinking_heartbeat = datetime.now().timestamp() + self.heartrate

            if datetime.now().timestamp() >= self.os_heartbeat:
                self.os_cycle()
                self.os_heartbeat = datetime.now().timestamp() + self.heartrate

    def think(self):
        """The process of incorporating stimuli into core memory, generating with that memory, and executing any tool calls in the response."""
        response_message = self.inference_backend.generate(core=self.prompt_engine.render_thought(self.core_memory),
                                                           tools=self.tool_engine.thought_tools)
        # add the generative response to the message history
        self.adust_recall_memory(response_message)

        # intentionally blocking
        if response_message.request_tools:
            self.handle_tool_execution(response_message.request_tools)
            self.thinking_heartbeat = 0 # always force an immediate generation after tool calls

    def os_cycle(self):
        """execute the system processes to keep the agent healthy"""
        garbage_collection = self.inference_backend.generate(
            core=self.prompt_engine.render_garbage_collection(self.core_memory),
            tools=self.tool_engine.os_tools
        )
        if garbage_collection.request_tools:
            self.handle_tool_execution(garbage_collection.request_tools)
            # don't need to adjust the heartbeat, only informative

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

    def handle_tool_execution(self, request_tools:List[ToolCall]) -> None:
        for tool_call in request_tools:
            # some kind of tool handler that merges internal tools with a tools folder in the downstream project
            tool_response:Message = self.tool_engine.execute(tool_call)
            self.stimuli_queue.append(tool_response)