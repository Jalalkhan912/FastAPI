from typing import Union, Optional

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "title of post 2", "content": "content of post 2", "id": 2}]

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_posts[-1]
    return {"latest_post": latest_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    for post in my_posts:
        if post['id'] == id:
            return {"post_detail": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            my_posts.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")


@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            my_posts[index] = updated_post.dict()
            my_posts[index]['id'] = id
            return {"data": my_posts[index]}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")