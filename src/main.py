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
from . import db
from . import demo
from .services import serve


SERVICES_DB: dict[str, Service] = {}

logger = logging.getLogger("uvicorn")

# setup lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager to handle application lifespan events.

    Used to load the database into memory.
    """
    global SERVICES_DB

    logger.info("Loading database...")
    SERVICES_DB = db.load_services(logger)

    yield

    logger.info("Saving database...")
    db.save_services(logger, SERVICES_DB)



# setup github oauth app
oauth = OAuth(config.configDict)
integrate_github_auth(oauth, config.configDict)

# setup FastAPI app
app = FastAPI(
    lifespan=lifespan
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
    services_list = []
    for id, service in SERVICES_DB.items():
        services_list.append({
            'id': id,
            'name': service.name,
            'description': service.description,
            'thumbnail_url': service.thumbnail_url
        }) 

    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": services_list,
    }


@app.get("/services/{service_id}", tags=["Services"])
async def list_service_info(
    current_user: Annotated[str, Depends(get_current_github_user)],
    service_id: Annotated[str, Path(title="The ID of the item to get")],
):

    service = SERVICES_DB.get(service_id)
    if not service:
        return {
            "status-code": HTTPStatus.NOT_FOUND,
            "message": HTTPStatus.NOT_FOUND.phrase,
            "details" : f"Service with id {service_id} not Found"
        }

    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": service,
    }


@app.post("/services", tags=["Services"])
async def create_service(
    current_user: Annotated[str, Depends(get_current_github_user)],
    payload: dict = {
        'name': 'Untitled',
        'parameters': [
            {
                'name': 'Untitled',
                'description': '',
                'data_type': '',
            }
        ],
        'description': '',
    }
):
    if not payload:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Payload is required"
        )

    new_service = Service(**payload)
    new_service_id = db.create_service(logger, SERVICES_DB, new_service)
    if not new_service_id:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Could not add service due to conflicting id."
        )

    response = new_service.model_dump()
    response['id'] = new_service_id
    return response

@app.patch("/services/{service_id}", tags=["Services"])
async def update_service(
    current_user: Annotated[str, Depends(get_current_github_user)],
    service_id: Annotated[str, Path(title="The ID of the item to get")],
    payload: dict,
):
    service = SERVICES_DB.get(service_id)
    if not service:
        return {
            "status-code": HTTPStatus.NOT_FOUND,
            "message": HTTPStatus.NOT_FOUND.phrase,
            "details" : f"Service with id {service_id} not found"
        }
    
    upd_service: Service
    try:
        upd_service = Service(**{**service.model_dump(), **payload})
    except ValidationError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Could not update service: check payload syntax."
        )

    SERVICES_DB[service_id] = upd_service
    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": upd_service.model_dump() | {"id": service_id}
    }


@app.delete("/services/{service_id}", tags=["Services"])
async def delete_service(
    current_user: Annotated[str, Depends(get_current_github_user)],
    service_id: Annotated[str, Path(title="The ID of the item to get")],
):

    removed = SERVICES_DB.pop(service_id, None)
    if not removed:
        return {
            "status-code": HTTPStatus.NOT_FOUND,
            "message": HTTPStatus.NOT_FOUND.phrase,
            "details": f"Service with id {service_id} not found"
        }

    return {
        "status-code": HTTPStatus.OK,
        "message": HTTPStatus.OK.phrase,
        "details": f"Service with id {service_id} deleted",
        "deleted": removed.model_dump()
    }

@app.post("/services/{service_id}/use", tags=["Services"])
async def use_service(
    current_user: Annotated[str, Depends(get_current_github_user)],
    service_id: Annotated[str, Path(title="The ID of the item to get")],
    payload: dict,
):

    service = SERVICES_DB.get(service_id)
    if not service:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Service with id {service_id} not found"
        )


    output = serve(service, payload, logger)

    if len(output.errors) == 0:
        return {
            "message": HTTPStatus.OK.phrase,
            "status-code": HTTPStatus.OK,
            "data": output
        }

    # if there are errors...
    expected_params = [ param.model_dump() for param in service.parameters] 
    raise HTTPException(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        detail={
            'service_id': service_id,
            'errors': output.errors,
            'input_data': payload,
            'expected_params': expected_params
        }
    )



@app.post("/demo/models/iris", tags=["Demo"])
async def use_iris(
    payload: demo.IrisPayload = demo.IrisPayload(
        petal_length=0,
        petal_width=0,
        sepal_length=0,
        sepal_width=0
    )
):
    try:
        return {
            "message": HTTPStatus.OK.phrase,
            "status-code": HTTPStatus.OK,
            "data": demo.serve_iris(payload, logger)
        }

    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    

@app.post("/demo/models/digits", tags=["Demo"])
async def use_digits(
    payload: demo.DigitsPayload = demo.DigitsPayload(
        pixels="0.0;0.0;10.0;16.0;16.0;11.0;0.0;0.0;0.0;1.0;11.0;"
                "7.0;6.0;16.0;3.0;0.0;0.0;0.0;0.0;0.0;10.0;15.0;0.0;0.0;"
                "0.0;0.0;0.0;0.0;15.0;7.0;0.0;0.0;0.0;0.0;0.0;0.0;15.0;"
                "9.0;0.0;0.0;0.0;0.0;0.0;0.0;7.0;13.0;0.0;0.0;0.0;0.0;"
                "5.0;4.0;10.0;16.0;0.0;0.0;0.0;0.0;10.0;16.0;16.0;10.0;0.0;0.0"
    )
):
    try:
        return {
            "message": HTTPStatus.OK.phrase,
            "status-code": HTTPStatus.OK,
            "data": demo.serve_digits(payload, logger)
        }
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
