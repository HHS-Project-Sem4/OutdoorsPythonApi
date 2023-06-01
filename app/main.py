from fastapi import FastAPI, HTTPException
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

    return {"message": "tester2"}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
