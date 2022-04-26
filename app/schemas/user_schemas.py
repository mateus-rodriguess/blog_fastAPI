from pydantic import BaseModel
from pydantic import EmailStr

class UserBase(BaseModel):
    email: EmailStr
   
    

class UserSchema(UserBase):
    first_name: str
    last_name: str
   
    class Config:
        orm_mode = True


class UserCreateSchema(UserSchema):
    password: str
    username: str
    class Config:
        orm_mode = False
