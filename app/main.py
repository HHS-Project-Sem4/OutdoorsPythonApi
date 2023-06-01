from fastapi import FastAPI
from test import test

app = FastAPI()


@app.get("/")
async def root():
    t = test()

    t.updateStar()
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
