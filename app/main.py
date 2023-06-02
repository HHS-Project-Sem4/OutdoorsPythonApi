from fastapi import FastAPI, Request

from app.test import test

app = FastAPI()

@app.get("/update")
async def root():
    print('START UPDATE')

    t = test()
    await t.updateStar()

    return {"message": "Updated"}


@app.get("/test")
async def root():
    print('START UPDATE')

    return {"message": "jk3456789"}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
