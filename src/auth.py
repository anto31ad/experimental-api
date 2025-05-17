import os

from typing import Annotated
from authlib.integrations.starlette_client import OAuth

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .schema import User, UserInDB, FAKE_USERS_DB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def integrate_github_auth(oauth: OAuth):
    oauth.register(
        name='github',
        client_id=os.getenv("GITHUB_CLIENT_ID"),
        client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize',
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'},
    )


def hash_password(password: str) -> str:
    return "fakehashed_"+password

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def decode_token(token) -> User | None:
    # NOTE: this is a stub method, no protection whatsoever
    return get_user(FAKE_USERS_DB, token)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    user = decode_token(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
