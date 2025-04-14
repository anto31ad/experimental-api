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

class User(BaseModel):
    username: str

class UserInDB(User):
    password: str

class Flower(BaseModel):
    sepal_length: float = 0
    sepal_width: float = 0
    petal_length: float = 0
    petal_width: float = 0
