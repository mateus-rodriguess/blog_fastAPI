from turtle import title
from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    summary: str

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True
