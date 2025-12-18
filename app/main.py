from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
models.Base.metadata.create_all(bind=engine)
from .routers import posts, users

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="Jk@#*123", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Error while connecting to database:", error)
        time.sleep(2)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}



app.include_router(posts.router)
app.include_router(users.router)

