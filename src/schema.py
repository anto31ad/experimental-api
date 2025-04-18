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
        "pathname": 'iris_classifier.pkl'
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
    output: str | None = None                           # description of the output
    pathname: str | None = None

class Flower(BaseModel):
    sepal_length: float = 0
    sepal_width: float = 0
    petal_length: float = 0
    petal_width: float = 0
