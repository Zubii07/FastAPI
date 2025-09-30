from pydantic import BaseModel


class BlogPost(BaseModel):
    title: str
    body: str
