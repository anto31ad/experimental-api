import logging

from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import Annotated
from pydantic import ValidationError

from starlette.middleware.sessions import SessionMiddleware

from authlib.integrations.starlette_client import OAuth

from fastapi import FastAPI, Depends, HTTPException, Path, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .utils import validate_url
from .auth import (
    integrate_github_auth,
    get_current_github_user,
)
from .schema import (
    User,
    Service
)

from . import config


SERVICES_DB: dict[str, Service] = {}

logger = logging.getLogger("uvicorn")

# setup lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager to handle application lifespan events.

    Used to load the database into memory.
    """
    #global SERVICES_DB

    logger.info("Loading database...")
    # SERVICES_DB = db.load_services(logger)

    logger.info(f"be: {config.THIS_PROCESS}")
    logger.info(f"fe: {config.FRONTEND_PROCESS}")

    yield

    logger.info("Saving database...")
    # db.save_services(logger, SERVICES_DB)



# setup github oauth app
oauth = OAuth(config.configDict)
integrate_github_auth(oauth, config.configDict)

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

@app.get('/login/github', tags=["Auth"])
async def login_with_github(request: Request, next_url: str="/docs"):

    # try to parse the redirect url
    if not validate_url(next_url, config.ALLOW_ORIGINS):
        logger.error(f"Invalid next_url during login: {next_url}")
        raise HTTPException(status_code=400, detail="Login failed because of invalid redirect URL")
    
    try:
        request.session['nextUrl'] = next_url
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

        next_url = request.session.pop('nextUrl', '/docs')
        return RedirectResponse(
            url=next_url)
    except Exception as exc:
        logger.error(f"GitHub callback error: {exc}")
        raise HTTPException(status_code=401, detail='GitHub denied authentication') 

@app.get('/logout', tags=["Auth"])
async def logout(request: Request, next_url: str = '/docs'):
    
    # try to parse the redirect url
    if not validate_url(next_url, config.ALLOW_ORIGINS):
        logger.error(f"Invalid next_url during logout: {next_url}")
        raise HTTPException(status_code=400, detail="Logout failed because of invalid redirect URL")

    try:
        request.session.clear()
        response = RedirectResponse(url=next_url)
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
    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": [
            {
                'id': 'iris',
                'name': 'iris',
                'description': 'description'
            },
            {
                'id': 'digits',
                'name': 'Digits Classifier',
                'description': 'description'
            }
        ],
    }

@app.get("/services/{item_id}", tags=["Services"])
async def get_service_info(
    current_user: Annotated[str, Depends(get_current_github_user)],
    item_id: str,
):
    
    if item_id != 'iris':
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=HTTPStatus.NOT_FOUND.phrase)

    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {
                'id': 'iris',
                'name': 'Iris Classifier',
                'description': 'description'
            },
    }
