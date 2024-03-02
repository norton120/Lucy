from lucy.backends.inference_backend_base import LucyInferenceBackendBase
from lucy.schema import Turn, Message, Role
# together uses a patched version of openai's client now
from .enums import LLMModel
from openai import OpenAI as Together


from lucy_mixtral_together_ai_backend.enums import LLMModel

class LucyTogetherAIBackend(LucyInferenceBackendBase):
    """LLM adapter for Mixtral 8x7b Together AI"""
    package_name = "sid_mixtral_together_ai_backend"
    model = LLMModel.codellama_34b_instruct# LLMModel.mixtral_8x7b_instruct
    client: "Together"
    core_memory_maximum_number_of_messages_in_history = 10
    core_memory_maximum_total_chars = 10000
    core_memory_maximum_chars_in_persona = 2000
    core_memory_maximum_chars_in_human = 2000
    core_memory_maximum_tool_count = 10

    def __init__(self,
                 api_key: str):
        """initiates the adapter with a model.
        Explicitly create with api_key to avoid lucye effects and opaque behavior.
        """
        self.client = Together(
            base_url = "https://api.together.xyz/v1",
            api_key = api_key,
            )

    def generate(self, turn:Turn) -> Turn:
        """Generates a response to complete the turn.
        """
        generation = self.client.chat.completions.create(
            model=self.model,
            messages=[m.model_dump(exclude_none=True) for m in turn.request_messages],
            tools=[t.model_dump(exclude_none=True) for t in turn.request_tools],
            tool_choice="auto",
        )
        # TODO: telementry
        response_message = Message(
            role=Role.assistant,
            content=generation.choices[0].message.content,
            tool_calls=generation.choices[0].message.tool_calls,
        )
        turn.response_message = response_message
        return turn