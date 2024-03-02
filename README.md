## Lucy

![Lucy](good_morning.gif)

_Applied design of the  MemGPT memory management strategy_


> [!IMPORTANT]
> Read all the README.md files in Lucy/lucy. This is becoming a full port of MemGPT to a production-able library that is backend-agnositc.
> We want light, modular and decoupled agent rendering using the brilliant paged memory design from MemGPT, but in a commerically viable implementation.
> Autogen may or may not be the multi-agent orchestrator of choice, we'll see when we get there.

### Why
We have a collection of use cases that need this. So Lucy is the abstraction where we figure this out together.

### Minimum Viable Capabilities
- **OSS Models Only**
  Must support VLLM/Ollama service. We can use Together.ai for testing initially with an eye on VLLM-OpenAI spec compatability
- **Perpetual chat with context recall**
  if you tell a Lucy agent that "I fucking love pickles" and later ask the agent or order me a sandwich, the bot should say "extra pickles, right?"
- **Agency via Python functions**
  a clean factory for providing agents with functions they can invoke and iterate with
- **Multi: User, Tenant, Agent**
  reflect almost every SaaS application on Earth - orgs/teams/companies have many users. Agents can differentiate between different users, different teams, and the relationship between the two.
  _note_: not multiplexing conversations. More than one human in the same conversation requires a completely different kind of model training that we haven't seen yet.
- **Task Solving**
  Agents can be given work to do and/or things to accomplish with the user, like getting status on a project or booking a flight.
- **grown-ass scalability**
  can be deployed in a container, scaled horizontally, load balanced, replicated across zones etc.

### Development
since Lucy is designed to drop into an application framework with orgs, venues, and users, you need frameworks to test it in.
- [fastapi_test](fastapi_test)
- `#TODO:` django_test

each is a basic instance of that framework where we can run a suite of Lucy tests in an agnostic way.


