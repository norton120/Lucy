### Lucy Project Architecture (NOT Library Arch)

! Warning ! Do not confuse the way the library is structured with the way a Lucy project is structured. Very different things.

When Lucy is installed in a project, it should look something like this:

```
lucy_project/
|
|\settings.py
|
|\__app/
|   |__app.py
|   |__router.py # app code etc
|
|\__templates/
|   |__personas/
|   |  | # custom persona not installed from packages
|   |
|   |__core/partials/_human.txt # if for some reason you want to tweak/edit the human template partial that ships with your given backend, you can just like a django override
|
|
|\__tools/
|   |_tool_1.py
|   |_tool_2.py
|
 \__src/
    | # bespoke modules
```

And the Lucy `settings.py` should look something like Djangos, like this:

```python3

class Settings(EnvSettings):

    # Memory
    # factory methods return a callable that takes the instance_id and memory type
    state_backend: RedisBackend.factory("redis0:6380,redis1:6380,allowAdmin=true")
    archive_backend: MongoBackend.factory("mongodb://localhost:27017/archive")
    recall_backend: RedisBackend.factory("redis0:6380,redis1:6380,allowAdmin=true")

    # LLMs
    inference_backends: {
        "general_purpose": MixtralTogetherAIBackend(model="Falcon-40b", api_key=self.together_ai_api_key),
        "coder": LLamaCoderTogetherAIBackend(model="wizard-140b", api_key=self.together_ai_api_key),
        "expert_in_fly_fishing": LLama2VertexBackend(model="custom-trained-flyfishing-model-10", b64_credentials=self.gcp_creds_as_b64)
    }
    default_inference_backend: "general_purpose"
```

Then you will build Lucy Egos like this:

```python3

from lucy.agent.stock_agents import Helper, ProjectManager
from lucy_elixir_phoenix import ElixirPhoenixCoder # plugin package for an elixir/phoenix developer agent
from lucy_sportsman.fishing import FlyFisher # plugin package for an agent that loves to fly fish

ego = Lucy(
    agents = [
        Helper(),
        Helper(), # extra grunt worker
        ProjectManager(spokesperson=True),
        ElixirPhoenixCoder(),
        FlyFisher()
    ],
    per_user = True, # each human has a 1:1 relationship with an ego
)

ego.attach_tool("lucy_project.tools.tool1.message_user") # add the ability for lucy to send messages back to the user!
ego.attach_tool("https://github.com/cool_lucy_tools/weather.git") # tool that enables Lucy to get weather data
ego.attach_tool("lucy_coffee_pot.coffee_pot") # tool package on pypi that allows you to toggle off and on some random guy's coffee pot at UCLA

ego.start() # ego runs perpetually as a daemon task

# but how to do users talk to our ego, and our ego talk to users? that's why Lucy is a library and not a project! that part is up to the project author.
# for example, maybe this is a fastapi implementation
@app.post("/")
def message_lucy(
    user: Depends[get_current_user],
    ego: Depends[get_lucy_ego]
):
    ego.message_from_user(user=user, message=message) # Lucy sends messages to the user all by himself with the `message_user` tool we gave him earlier!

Under the hood, each agent has a `stimuli` queue where all new information - messages from users, responses from tools, and warnings from the  lucy OS about memory size - are enqued.

```