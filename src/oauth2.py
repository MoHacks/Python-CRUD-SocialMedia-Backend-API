
import jwt
from jwt.exceptions import InvalidTokenError
# from jose import JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from . import schemas, db, dbmodels, utils
# from .. import outh2_scheme
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # login endpoint will be used as tokenUrl

# Creates the access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Verifies if the token is valid
def verify_access_token(token: str, credentials_exception):

    try:
        # decode jwt
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # extract id
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        # valid with the schema the token id with the id of the user
        token_data = schemas.TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception

    return token_data

# returns the User object if valid token is provided
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(db.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    # print("token: ", token)
    user = db.query(dbmodels.User).filter(dbmodels.User.id == token.id).first()

    return user