from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from schema import User, UserInDB, FAKE_USERS_DB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str) -> str:
    return "fakehashed_"+password

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def decode_token(token) -> User:
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
