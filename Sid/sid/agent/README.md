## Sid Agent

This module handles the mechanical orchestration of LLM calls, function calls and memory calls that make an Agent's [Freudian _Id_](https://en.wikipedia.org/wiki/Id,_ego_and_superego) actually operate.

Sid `agent` needs to handle
- assembling memory tiers based on the interacting user and context
- compiling prompts based on the current state of each memory tier, the available tools, and the user message
- dispatching compiled prompts to the LLM
- processing the responses including executing internal Sid function calls and tool calls, from the response


**Dev Notes:**

- Agent functions on infinately recursive, dispatching function calls, messages to user(s) etc as side effects during the perpetual event loop.
- Agent tools (external functions) and memory/compiler/dispatcher processes must be implementation-agnostic - the agent should have no implementation details of what LLM it is using, what memory backends are in place etc. Build standard interfaces, make plugins available.
