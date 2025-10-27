from typing import Union, Optional

from fastapi import FastAPI
from fastapi.params import Body

from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}


@app.get("/posts")
def get_posts():
    return {"posts": "post1"}

@app.post("/createposts")
def create_post(post: Post):
    print(post)
    print(post.dict())
    return {"data": post}