from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.test import test

app = FastAPI()

@app.get("/update")
async def root():
    print('START UPDATE')

    t = test()
    t.updateStar()

    return {"message": "Updated"}


@app.get("/test")
async def root():
    print('START UPDATE')

    return {"message": "jk"}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
