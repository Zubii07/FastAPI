from pydantic import BaseModel, Field, validator
from typing import List, Optional

class BlogPost(BaseModel):
    title: str
    body: str

class Blog(BlogPost):
    class Config:
        from_attributes = True

class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUserBase(BaseModel):
    name: str
    email: str
    class Config:
        from_attributes = True

class ShowBlogBase(BaseModel):
    title: str
    body: str
    class Config:
        from_attributes = True

class ShowUser(ShowUserBase):
    blogs: List[ShowBlogBase] = []
    class Config:
        from_attributes = True

class ShowBlog(ShowBlogBase):
    creator: ShowUserBase
    class Config:
        from_attributes = True

