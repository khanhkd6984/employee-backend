import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from . import models
from . import crud
from . import schemas
from . import database

load_dotenv()


# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(
#         to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM")
#     )
#     return encoded_jwt


# def get_current_user(
#     db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(
#             token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
#         )
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#         token_data = schemas.TokenData(email=email)
#     except JWTError:
#         raise credentials_exception
#     user = crud.get_user_by_email(db, email=token_data.email)
#     if user is None:
#         raise credentials_exception
#     return user


def verify_zoho_user(token: str, db: Session = Depends(database.get_db)):
    res = requests.get(
        "https://accounts.zoho.com/oauth/user/info",
        headers={"Authorization": token},
    )
    if res.status_code == 200:
        email = res.json().get("Email", None)
        db_user = crud.get_user_by_email(db, email)
        return db_user if db_user else False
    return False
