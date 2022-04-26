
from sqlalchemy import Column, Integer, String, Boolean

from app.database import Base


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    #is_active = Column(Boolean, default=True)