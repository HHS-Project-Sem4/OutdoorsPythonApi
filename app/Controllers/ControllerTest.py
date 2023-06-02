from app.main import app


@app.get("/eb")
async def root():
    return {"message": "eb"}


@app.get("/lel")
async def say_hello():
    return {"message": "lel"}
