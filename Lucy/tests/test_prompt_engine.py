from pytest import mark as m
from lucy.agent.prompt_engine import PromptEngine
from stub_llm_backend import StubLLMBackend

@m.describe("When the prompt engine assembles prompts")
class TestPromptEngine:
    """tests that prompts compile as expected"""

    @m.it("should compile the default core prompts without error")
    def test_default_core_compiles(self):
        prompt_args = {
            "human_chars": 50,
            "human_chars_limit":1000,
            "persona_chars": 76,
            "persona_chars_limit": 1000,
            "count_visible_messages": 4,
            "count_total_messages": 15
        }
        engine = PromptEngine("stub_llm_backend")
        rendered = engine.render_core("core", **prompt_args)
        print(rendered)
        assert rendered