import os
from lucy.schema import Turn, Message, Role, Tool

from lucy_mixtral_together_ai_backend.main import LucyMixtralTogetherAIBackend

class TestGenerates:

    mta = LucyMixtralTogetherAIBackend(
        api_key=os.environ["TOGETHER_API_KEY"]
    )
    system = Message(
        role=Role.system,
        content=("You are a helpful assistant that can access external functions. The responses of these functions will be appended to this dialog. Provide the user with the best possible response, using the information from these function calls when necessary.")
                 #"Only call these functions when they are needed and helpful."),
    )
    request = Message(
        role=Role.user,
        content="I am Dave. Who is my boss?",
    )
    turn = Turn(
        request_messages = [system, request],
        request_tools=[Tool(type="function",
                            name="company_org_chart",
                            description="returns the org chart including names, positions, and hierarchy for the company, formatted in xml.")]
    )
    response = mta.generate(turn)
    assert response.response_message.tool_calls