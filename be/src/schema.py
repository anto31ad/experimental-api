from pydantic import BaseModel

class User(BaseModel):
    username: str

class GitHubUser(User):
    github_id: str

class ServiceParameter(BaseModel):
    name: str
    description: str | None = None

# NOTE: order of parameters matters!
# imagine the model expecting parameters (A, B), both floats;
# if the API sends values for (b, A) for (A, B), it will produce unexpected results
class Service(BaseModel):
    name: str | None = None                             # name of the service
    description: str | None = None                      # a brief description of the service
    parameters: list[ServiceParameter] = []             # description of the required fields
    thumbnail_url: str | None = None                    # a decorative image
    executable_url: str | None = None                   # the url of the executable

class ServiceOutput(BaseModel):
    input_payload: dict = {}
    output: dict = {}
    errors: list = []
