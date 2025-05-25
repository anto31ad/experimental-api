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
                    "data_type" : "float"
                },
                {
                    "name": "petal_width",
                    "data_type" : "float"
                },
                {
                    "name": "sepal_length",
                    "data_type" : "float"
                },
                {
                    "name": "sepal_width",
                    "data_type" : "float"
                },
            ],
        "description": "predicts Iris subspecies from petal and sepal widths and lengths",
        "path_to_model": 'data/iris_classifier.pkl',
        "thumbnail_url": '/static/iris-thumb.jpg'
    },
    2 : {
        "id": 2,
        "name": "8x8 Handwritten Digits Recognizer",
        "parameters":
            [
                {
                    "name": "pixels",
                    "description": "An array of 64 values, each representing a pixel's opacity.",
                    "data_type" : "str"
                },
            ],
        "description": "Predicts a digit (0-9) from handwritten representation on a canvas of 8x8 pixels",
        "outputs": "predicted digit",
        "path_to_model": 'data/digit-classifier.pkl'
    }
}

class User(BaseModel):
    username: str

class UserInDB(User):
    password: str

class GitHubUser(User):
    github_id: str

class ServiceParameter(BaseModel):
    name: str
    description: str | None = None
    data_type: str | None = None

class Service(BaseModel):
    id: int
    name: str | None = None                             # name of the service
    description: str | None = None                      # a brief description of the service
    parameters: list[ServiceParameter] | None = None    # description of the required fields
    thumbnail_url: str | None = None                    # a decorative image

class ServiceOutput(BaseModel):
    input_payload: dict = {}
    output: dict = {}
    errors: list[str] = []
