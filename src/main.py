# NOTE: param 'current_user' is not used in several functions;
#       However, it is needed for calling Depends, which in turn
#       enforces authentication, so only verified users can call this method
import logging

from http import HTTPStatus
from typing import Annotated

from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware

from authlib.integrations.starlette_client import OAuth

from fastapi import FastAPI, Depends, HTTPException, Path, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .auth import (
    integrate_github_auth,
    get_current_user,
    get_current_github_user,
    hash_password
)
from .schema import (
    User,
    UserInDB,
    FAKE_USERS_DB,
    FAKE_SERVICES_DB,
    Service
)
from .services import serve

app = FastAPI()
logger = logging.getLogger("uvicorn")

# Prevents CORS error when browsers receive a response from this 
# "*" means "all"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key="!secret")  # Use a real secret key in production

# load environment variables
config = Config('.env')

# setup github oauth app
oauth = OAuth(config)
integrate_github_auth(oauth)


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

    hashed_password = hash_password(form_data.password)

    if not hashed_password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get('/login/github')
async def login_with_github(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await oauth.github.authorize_redirect(request, redirect_uri)


@app.get('/auth/github')
async def auth_callback(request: Request):
    token = await oauth.github.authorize_access_token(request)
    user = await oauth.github.get('user', token=token)
    user_data = user.json()

    # store user temporarily
    request.session['user'] = {
        "github_id": user_data["id"],
        "username": user_data["login"],
    }
    return RedirectResponse(url="/docs")


@app.get('/logout')
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/docs")


# ==============================================================
# USERS
# ==============================================================
@app.get("/users/me", tags=["Users"])
async def read_current_user(
    current_user: Annotated[User, Depends(get_current_github_user)]
):
    return current_user


# ==============================================================
# SERVICES
# ==============================================================

@app.get("/services", tags=["Services"])
async def list_available_services(
    current_user: Annotated[str, Depends(get_current_github_user)]
):
    services_list = list(FAKE_SERVICES_DB.values())

    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": services_list,
    }


@app.get("/services/{service_id}", tags=["Services"])
async def list_service_info(
    current_user: Annotated[str, Depends(get_current_github_user)],
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
    current_user: Annotated[str, Depends(get_current_github_user)],
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
