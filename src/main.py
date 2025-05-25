import logging

from http import HTTPStatus
from typing import Annotated

from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware

from authlib.integrations.starlette_client import OAuth

from fastapi import FastAPI, Depends, HTTPException, Path, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

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

# load environment variables
config = Config('.env')

FRONTEND_ORIGIN: str = f"http://{config.get('FRONTEND_HOST')}:{config.get('FRONTEND_PORT')}"

# setup github oauth app
oauth = OAuth(config)
integrate_github_auth(oauth)

# setup FastAPI app
app = FastAPI()
logger = logging.getLogger("uvicorn")
    # Prevents CORS error when browsers receive a response from this 
    # "*" means "all"
app.add_middleware(
    CORSMiddleware,

    # If allow_credentials is True, allow_origins cannot be ["*"], because
    # when the browser makes a request with credentials (e.g. read-only cookie),
    # this server would send a response with header "Access-Control-Allow-Origin: *"
    # which is not allowed by the CORS specification.
    allow_credentials=True,
    allow_origins=[FRONTEND_ORIGIN],

    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    SessionMiddleware,
    secret_key="!secret")  # TODO Use a real secret key in production

    # mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# ==============================================================
# GENERAL
# ==============================================================
@app.get("/")
async def root():
    return {"message": "Hello World"}


# ==============================================================
# AUTHENTICATION
# ==============================================================

# @app.post("/token", tags=["Auth"])
# async def login(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ):
#     user_dict = FAKE_USERS_DB.get(form_data.username)

#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)

#     hashed_password = hash_password(form_data.password)

#     if not hashed_password == user.password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     return {"access_token": user.username, "token_type": "bearer"}


@app.get('/login/github', tags=["Auth"])
async def login_with_github(request: Request):
    try:
        redirect_uri = request.url_for('auth_callback')
        return await oauth.github.authorize_redirect(request, redirect_uri)
    except Exception as exc:
        logger.error(f"GitHub login error: {exc}")
        raise HTTPException(status_code=401, detail='Login failed while reaching GitHub') 


@app.get('/auth/github', tags=["Auth"])
async def auth_callback(request: Request):
    try:
        token = await oauth.github.authorize_access_token(request)
        github_response = await oauth.github.get('user', token=token)
        github_user_data = github_response.json()

        # store user temporarily
        user_data = {
            "github_id": github_user_data["id"],
            "username": github_user_data["login"],
        }
        request.session['user'] = user_data
        return RedirectResponse(
            url=f"{FRONTEND_ORIGIN}/login/callback")
    except Exception as exc:
        logger.error(f"GitHub callback error: {exc}")
        raise HTTPException(status_code=401, detail='GitHub denied authentication') 


@app.get('/logout', tags=["Auth"])
async def logout(request: Request):
    try:
        request.session.clear()
        response = RedirectResponse(url=FRONTEND_ORIGIN)
        response.delete_cookie('session')
        return response
    except Exception as exc:
        logger.error(f"logout error: {exc}")
        raise HTTPException(status_code=400, detail='Something failed during logout') 
       

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

# NOTE: param 'current_user' may not used in the following path operations;
#       However, it is needed for calling Depends, which in turn enforces authentication,
#       this makes sure that only verified users can call this method

@app.get("/services", tags=["Services"])
async def list_available_services(
    current_user: Annotated[str, Depends(get_current_github_user)]
):
    services_list = [
        Service(**service_dict) for service_dict in FAKE_SERVICES_DB.values()
    ]

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
