import os

from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from fastapi import HTTPException, status, Request

async def is_logged_in(request: Request):
    
    session = request.session
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in",
        )
