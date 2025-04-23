# NOTE: param 'current_user' is not used in several functions;
#       However, it is needed for calling Depends, which in turn
#       enforces authentication, so only verified users can call this method

import logging

from http import HTTPStatus
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordRequestForm

import auth
from schema import (
    User,
    UserInDB,
    FAKE_USERS_DB,
    FAKE_SERVICES_DB,
    Service
)
from services import serve

app = FastAPI()
logger = logging.getLogger("uvicorn")


# ==============================================================
# GENERAL
# ==============================================================
@app.get("/")
async def root():
    return {"message": "Hello World"}


# ==============================================================
# AUTHENTICATION
# ==============================================================
@app.post("/token", tags=["Auth"])
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


# ==============================================================
# USERS
# ==============================================================
@app.get("/users/me", tags=["Users"])
async def read_current_user(
    current_user: Annotated[User, Depends(auth.get_current_user)]
):
    return current_user


# ==============================================================
# SERVICES
# ==============================================================

@app.get("/services", tags=["Services"])
async def list_available_services(
    current_user: Annotated[str, Depends(auth.get_current_user)]
):
    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": FAKE_SERVICES_DB,
    }


@app.get("/services/{service_id}", tags=["Services"])
async def list_service_info(
    current_user: Annotated[str, Depends(auth.get_current_user)],
    service_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
):

    service_dict = FAKE_SERVICES_DB.get(service_id)
    if not service_dict:
        return {
            "status-code": HTTPStatus.NOT_FOUND,
            "message": HTTPStatus.NOT_FOUND.phrase,
            "details" : f"Service with id {service_id} not Found"
        }
    
    service = Service(**service_dict)

    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": service,
    }


@app.post("/services/{service_id}", tags=["Services"])
async def predict(
    current_user: Annotated[str, Depends(auth.get_current_user)],
    service_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    payload: dict,
):

    service_dict = FAKE_SERVICES_DB.get(service_id)
    if not service_dict:
        return {
            "status-code": HTTPStatus.NOT_FOUND,
            "message": HTTPStatus.NOT_FOUND.phrase,
            "details" : f"Service with id {service_id} not found"
        }

    service = Service(**service_dict)
    output = serve(service, payload, logger)

    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": output
    }
