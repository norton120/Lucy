
# together uses a patched version of openai's client now
from openai import OpenAI as Together


from sid_mixtral_together_ai_backend.enums import LLMModel

class SidTogetherAIBackend:
    """LLM adapter for Together AI"""
    client: "Together"

    def __init__(self,
                 model: LLMModel,
                 api_key: str):
        """initiates the adapter with a model.
        Explicitly create with api_key to avoid side effects and opaque behavior.
        """
        self.client = Together(
            base_url = "https://api.together.xyz/v1",
            api_key = api_key,
            model = model.value
            )

    def generate(self, )