### Sid Project Architecture (NOT Library Arch)

! Warning ! Do not confuse the way the library is structured with the way a Sid project is structured. Very different things.

When Sid is installed in a project, it should look something like this:

```
sid_project/
|
|\settings.py
|
|\__app/
|   |__app.py
|   |__router.py # app code etc
|
|\__personas/
|   |__salesperson/
|      | # custom persona not installed from packages
|
|\__tools/
|   |_tool_1.py
|   |_tool_2.py
|
 \__src/
    | # bespoke modules
```

And the Sid `settings.py` should look something like Djangos, like this:

```python3

class Settings(EnvSettings):

    # Memory
    state_backend: RedisBackend("redis0:6380,redis1:6380,allowAdmin=true")
    archive_backend: MongoBackend("mongodb://localhost:27017/archive")
    recall_backend: RedisBackend("redis0:6380,redis1:6380,allowAdmin=true")

    # LLMs
    generative_backends: {
        "general_purpose": TogetherAIBackend(model="Falcon-40b", api_key=self.together_ai_api_key),
        "coder": TogetherAIBackend(model="wizard-140b", api_key=self.together_ai_api_key),
        "expert_in_fly_fishing": VertexBackend(model="custom-trained-flyfishing-model-10", b64_credentials=self.gcp_creds_as_b64)
    }
    default_generative_backend: "general_purpose"
```

Then you will build Sid Egos like this:

```python3

from sid.agent.stock_agents import Helper, ProjectManager
from sid_elixir_phoenix import ElixirPhoenixCoder # plugin package for an elixir/phoenix developer agent
from sid_sportsman.fishing import FlyFisher # plugin package for an agent that loves to fly fish

ego = Sid(
    agents = [
        Helper(),
        Helper(), # extra grunt worker
        ProjectManager(spokesperson=True),
        ElixirPhoenixCoder(),
        FlyFisher()
    ],
    per_user = True, # each human has a 1:1 relationship with an ego
)

ego.attach_tool("sid_project.tools.tool1.message_user") # add the ability for sid to send messages back to the user!
ego.attach_tool("https://github.com/cool_sid_tools/weather.git") # tool that enables Sid to get weather data
ego.attach_tool("sid_coffee_pot.coffee_pot") # tool package on pypi that allows you to toggle off and on some random guy's coffee pot at UCLA

ego.start() # ego runs perpetually as a daemon task

# but how to do users talk to our ego, and our ego talk to users? that's why Sid is a library and not a project! that part is up to the project author.
# for example, maybe this is a fastapi implementation
@app.post("/")
def message_sid(
    user: Depends[get_current_user],
    ego: Depends[get_sid_ego]
):
    ego.message_from_user(user=user, message=message) # Sid sends messages to the user all by himself with the `message_user` tool we gave him earlier!
```