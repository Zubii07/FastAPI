from pydantic import BaseModel, Field, validator
from typing import List

class BlogPost(BaseModel):
    title: str
    body: str

class Blog(BlogPost):
    class Config:
        attributes = True

class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List
    class Config:
        from_attributes = True



class ShowBlog(BaseModel):
    # write here what you want to show. for example
    title: str
    body: str
    creator: ShowUser
    class Config:
        from_attributes = True

