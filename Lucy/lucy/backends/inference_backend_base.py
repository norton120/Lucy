from abc import ABC, abstractmethod

from lucy.schema import Turn

class LucyInferenceBackendBase(ABC):
    """All Inference backends must implement this interface.

    Inference backends are the coupled assembly of a model, the prompt templates for that model, and the the LLM server where the model runtime exists.
    """

    ### Required attributes ###
    @property
    @abstractmethod
    def package_name(self) -> str:
        """The name of the package that this backend belongs to.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def model(self) -> str:
        """The name of the model that this backend is using.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def core_memory_maximum_number_of_messages_in_history(self) -> int:
        """The maximum number of messages to include in the core memory at one time.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def core_memory_maximum_total_chars(self) -> int:
        """The maximum number of characters to include in the core memory at one time.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def core_memory_maximum_chars_in_persona(self) -> int:
        """The maximum number of characters to include in the core memory persona section at one time.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def core_memory_maximum_chars_in_human(self) -> int:
        """The maximum number of characters to include in the core memory human section at one time.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def core_memory_maximum_tool_count(self) -> int:
        """The maximum number of tools to include in the core memory at one time.
        """
        raise NotImplementedError

    ### Optional attributes ###

    @property
    def templates_directory(self) -> str:
        """The relative pathname within the package where all templates and partials live.
        You should have a _really good reason_ for changing this!
        """
        return "templates"

    ### Required methods ###

    @abstractmethod
    def generate(self, turn:Turn) -> Turn:
        """Processes the turn against the inference model to complete it, returning the completed turn instance.
        """
        raise NotImplementedError


    ### These methods are generally fine to inherit ###

    @property
    def prompt_engine_args(self) -> tuple:
        """returns the arguments to pass to the prompt engine.
        """
        return (self.package_name, self.templates_directory,)