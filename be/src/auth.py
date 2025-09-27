import os

from jose import jwt
from fastapi import HTTPException, Depends

from . import config

async def get_current_user(token: str = Depends(config.oauth2_scheme)):
    try:
        # Decode and validate the JWT
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=["HS256"])
        user_data = {
            "github_id": payload.get("github_id"),
            "username": payload.get("username")
        }
        if not user_data["github_id"]:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return user_data
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
