from typing import Literal
from pydantic import BaseModel

FAKE_USERS_DB = {
    "admin": {
        "username": "admin",
        "password": "fakehashed_secret",
    },
    "alice": {
        "username": "alice",
        "password": "fakehashed_secret2",
    },
}

# NOTE: order of parameters matters!
# imagine the model expecting parameters (A, B), both floats;
# if the API sends values for (b, A) for (A, B), it will produce unexpected results
FAKE_SERVICES_DB: dict = {
    1 : {
        "id": 1,
        "name": "Iris Subspecies Classifier",
        "parameters":
            [
                {
                    "name": "petal_length",
                    "expects" : "float"
                },
                {
                    "name": "petal_width",
                    "expects" : "float"
                },
                {
                    "name": "sepal_length",
                    "expects" : "float"
                },
                {
                    "name": "sepal_width",
                    "expects" : "float"
                },
            ],
        "path_to_model": 'data/iris_classifier.pkl'
    },
    2 : {
        "id": 2,
        "name": "8x8 Handwritten Digits Recognizer",
        "parameters":
            [
                {
                    "name": "features",
                    "expects" : "str"
                },
            ],
        "outputs": "predicted digit",
        "path_to_model": 'data/digit-classifier.pkl'
    }
}

class User(BaseModel):
    username: str

class UserInDB(User):
    password: str

class Payload(BaseModel):
    data: dict

class ServiceParameter(BaseModel):
    name: str
    expects: Literal['int', 'str', 'float', 'bool', 'dict', 'list']

class Service(BaseModel):
    id: int
    name: str | None = None                             # name of the service
    parameters: list[ServiceParameter] | None = None    # description of the required fields
    outputs: str | None = None                          # description of the output
    path_to_model: str | None = None

class ServiceOutput(BaseModel):
    input_payload: dict = {}
    output: dict = {}
    errors: list[str] = []
