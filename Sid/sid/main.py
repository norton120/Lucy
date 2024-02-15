from memgpt import MemGPT
from memgpt.data_types import LLMConfig
from sid.settings import settings

together_ai_llm = LLMConfig(
  model_endpoint_type="together_ai",
  model="togethercomputer/falcon-7b-instruct",
  model_endpoint="https://api.together.xyz/v1",
)

class Sid:

  def __init__(self):
    self.client = MemGPT(
      quickstart="openai", # yay together.ai/VLLM have a comp
      config={
        "openai_api_key": settings.together_ai_key,
        "default_llm_config": together_ai_llm
      }
    )

    self.agent = self.client.create_agent(
        agent_config={
          "persona": "sam_pov",
          "human": "cs_phd",
        }
    )

  def turn(self, message:str):
    return self.client.user_message(agent_id=self.agent.id, message=message)