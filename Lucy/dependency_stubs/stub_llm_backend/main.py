from lucy.backends.inference_backend_base import LucyInferenceBackendBase


class StubLLMBackend(LucyInferenceBackendBase):
    """A non-functional LLM Backend for testing (to keep us honest and decoupled)"""
