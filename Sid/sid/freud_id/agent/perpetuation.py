from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sid.freud_id.agent import Agent

class Perpetuation:
    """The mechanics for an Agent "conciousness." A self-healing loop of adjusting memory, reacting to stimuli, and generating responses."""

    def __init__(self, agent:"Agent"):
        self.agent = agent

    # heartbeat lives here

    def start(self):

        while True:
            user_message = self.agent.message_queue.deque()
