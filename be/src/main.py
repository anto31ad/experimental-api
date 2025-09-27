import logging
import requests

from typing import Annotated
from contextlib import asynccontextmanager
from http import HTTPStatus
from jose import jwt
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth

from fastapi import FastAPI, Depends, HTTPException, Path, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .utils import validate_url, fetch_service_info
from .auth import (
    get_current_user
)
from .schema import (
    User,
)

from . import config

logger = logging.getLogger("uvicorn")

# setup lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager to handle application lifespan events.

    Used to load the database into memory.
    """
    logger.info(f"be: {config.THIS_PROCESS}")
    logger.info(f"fe: {config.FRONTEND_PROCESS}")

    yield

    logger.info("Shutting down...")


# setup github oauth app
oauth = OAuth(config.configDict)
oauth.register(
    name='github',
    client_id=config.GITHUB_CLIENT_ID,
    client_secret=config.GITHUB_CLIENT_SECRET,
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

# setup FastAPI app
app = FastAPI(
    lifespan=lifespan,
    title='Experimental API'
)
    # Prevents CORS error when browsers receive a response from this 
    # "*" means "all"
app.add_middleware(
    CORSMiddleware,

    # If allow_credentials is True, allow_origins cannot be ["*"], because
    # when the browser makes a request with credentials (e.g. read-only cookie),
    # this server would send a response with header "Access-Control-Allow-Origin: *"
    # which is not allowed by the CORS specification.
    allow_credentials=True,
    allow_origins=config.ALLOW_ORIGINS,

    allow_methods=["*"],
    allow_headers=["*"],
)

# session middleware is needed by oauth
app.add_middleware(
    SessionMiddleware,
    secret_key=config.JWT_SECRET_KEY)

# ==============================================================
# ROOT
# ==============================================================
@app.get("/")
async def root():
    return {"message": "Hello World"}


# ==============================================================
# AUTHENTICATION
# ==============================================================

@app.get('/login/github', tags=["Auth"])
async def login_with_github(request: Request, next_url: str="/docs"):
    # try to parse the redirect url
    if not validate_url(next_url, config.ALLOW_ORIGINS):
        logger.error(f"Invalid next_url during login: {next_url}")
        raise HTTPException(status_code=400, detail="Login failed because of invalid redirect URL")
    
    try:
        redirect_uri = request.url_for('github_auth_callback')
        request.session['targetUrl'] = next_url
        return await oauth.github.authorize_redirect(request, redirect_uri)
    except Exception as exc:
        logger.error(f"GitHub login error: {exc}")
        raise HTTPException(status_code=401, detail='Login failed while reaching GitHub') 


@app.get('/auth/github', tags=["Auth"])
async def github_auth_callback(request: Request):
    try:
        token = await oauth.github.authorize_access_token(request)
        github_response = await oauth.github.get('user', token=token)
        github_user_data = github_response.json()

        # store user temporarily
        user_data = {
            "github_id": github_user_data["id"],
            "username": github_user_data["login"],
        }
        # Generate a JWT token
        jwt_token = jwt.encode(
            user_data,
            config.JWT_SECRET_KEY,
            algorithm="HS256"
            # TODO token lifetime    
        )

        # construct redirect response
        target_url = request.session['targetUrl']
        full_target_url = f"{target_url}?token={jwt_token}"
        return RedirectResponse(
            url=full_target_url)

    except Exception as exc:
        logger.error(f"GitHub callback error: {exc}")
        raise HTTPException(status_code=401, detail='GitHub denied authentication') 

# ==============================================================
# USERS
# ==============================================================
@app.get("/users/me", tags=["Users"])
async def read_current_user(
    current_user: Annotated[User, Depends(get_current_user)]
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
    current_user: Annotated[User, Depends(get_current_user)]
):

    try:    
        services_response: dict = requests.get(f'{config.GATEWAY_PROCESS}/services').json()
        services_list = []
        for item in services_response.values():
            services_list.append(item['Service'])
    except:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=HTTPStatus.NOT_FOUND.phrase)

    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": services_list
    }

@app.get("/services/{service_id}", tags=["Services"])
async def get_service_info(
    service_id: str,
    current_user: Annotated[User, Depends(get_current_user)]
):
    service_info: dict | None = fetch_service_info(service_id)
    if not service_info:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=HTTPStatus.NOT_FOUND.phrase)

    service_info['id'] = service_id
    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": service_info
    }

@app.post("/services/{service_id}", tags=["Services"])
async def use_service(
    service_id: str,
    payload: dict,
    current_user: Annotated[User, Depends(get_current_user)]
):
    response = requests.post(
        url=f'{config.GATEWAY_PROCESS}/{service_id}/use',
        json=payload)
    
    if not response.ok:
        logger.info("Response not ok")
        raise HTTPException(
            status_code=response.status_code,
            detail=response.content
        )

    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": response.json()['data']
    }
