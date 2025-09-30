from pydantic import BaseModel


class BlogPost(BaseModel):
    title: str
    body: str


class ShowBlog(BlogPost):
    # write here what you want to show. for example
    # id: int
    class Config:
        from_attributes = True
