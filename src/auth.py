import os

from authlib.integrations.starlette_client import OAuth

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer

from .schema import GitHubUser

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


async def get_current_github_user(request: Request) -> GitHubUser:
    user = request.session.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return GitHubUser(
        # using a str cast to sanitize values;
        # e.g. the github user id is a integer, but GitHubUser wants a str 
        username=str(user["username"]),
        github_id=str(user["github_id"]),
    )
