import pickle
import logging

from http import HTTPStatus
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

import auth
from schema import User, UserInDB, Flower, FAKE_USERS_DB

app = FastAPI()
logger = logging.getLogger("uvicorn")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user_dict = FAKE_USERS_DB.get(form_data.username)

    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)

    hashed_password = auth.hash_password(form_data.password)

    if not hashed_password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_current_user(
    current_user: Annotated[User, Depends(auth.get_current_user)]
):
    return current_user

@app.post("/predict")
def predict(
    features: Flower,
    current_user: Annotated[str, Depends(auth.get_current_user)]
):
    # param 'current_user' is not used in this function;
    # However, it is needed for calling Depends, which in turn
    # enforces authentication, so only verified users can call this method

    with open('data/model.pkl', 'rb') as file:
        logger.info("Attempting to load model")
        model = pickle.load(file)

    raw_prediction = model.predict(
        [
            [
                features.sepal_length,
                features.sepal_width,
                features.petal_length,
                features.petal_width,
            ]
        ]
    )
    prediction = int(raw_prediction[0])

    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {
            "features": {
                "sepal_length": features.sepal_length,
                "sepal_width": features.sepal_width,
            },
            "prediction_id": prediction,
        },
    }
