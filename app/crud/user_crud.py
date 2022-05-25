from typing import Optional, List

from sqlalchemy.orm import Session
from app.models.user_models import UserModel
from app.schemas.user_schemas import UserCreateSchema, UserSchema
from app.services.security import get_password_hash


def get_all_users(db: Session) -> List[UserModel]:
    return db.query(UserModel).filter().all()


def get_user_by_username(db: Session, username: str) -> Optional[UserModel]:
    return db.query(UserModel).filter(UserModel.username == username).first()


def add_user(db: Session, user_data: UserCreateSchema) -> UserSchema:
    hashed_password = get_password_hash(user_data.password)
    db_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, email) -> UserSchema:
    db.delete(email=email)
    db.commit()