from pydantic import BaseModel, Field, validator


class BlogPost(BaseModel):
    title: str
    body: str


class ShowBlog(BaseModel):
    # write here what you want to show. for example
    # id: int
    class Config:
        from_attributes = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    class Config:
        from_attributes = True

