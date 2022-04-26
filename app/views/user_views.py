from datetime import timedelta
from hashlib import new
from os import access
from typing import List

from app.crud import user_crud
from app.database import get_db
from app.models.user_models import UserModel
from app.schemas.token_schemas import TokenDataSchema
from app.schemas.user_schemas import UserCreateSchema, UserSchema
from app.services.security import ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user, authenticate_user, create_access_token

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

user_router = APIRouter()


@user_router.get("", response_model=List[UserSchema])
async def users(db: Session = Depends(get_db)):
    users = user_crud.get_all_users(db)
    return list(users)


@user_router.get("/{email:str}", response_model=UserSchema)
async def get_user(email: str, db: Session = Depends(get_db)) -> UserSchema:
    user = user_crud.get_user_by_email(db, email)
    if user:
        return user
    else:
        return {'message': 'user not found'}, 404


@user_router.post("/login", response_model=TokenDataSchema)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("me", response_model=UserSchema)
async def get_current_user(user_data: UserModel = Depends(get_current_user)):
    return user_data


@user_router.post("/sign/up", response_model=UserSchema)
async def sign_up(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, user_data.email)

    if user:
        raise HTTPException(
            status_code=409,
            detail="email exist",
        )
    new_user = user_crud.add_user(db, user_data)
    return new_user