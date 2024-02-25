from enum import Enum

class LLMModel(str, Enum):
    mixtral_8x7b_instruct = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    mixral_7b_instruct = "mistralai/Mistral-7B-Instruct-v0.1"
    codellama_34b_instruct = "togethercomputer/CodeLlama-34b-Instruct"