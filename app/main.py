from fastapi import FastAPI
from app.test import test

app = FastAPI()


@app.get("/update")
async def root():
    print('START UPDATE')

    t = test()
    t.updateStar()

    return {"message": "updating"}


@app.get("/test")
async def root():
    print('START UPDATE')

    return {"message": "tester"}

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
