from fastapi import FastAPI

from app.data.Updater import Updater

app = FastAPI()

@app.get("/updateStar")
async def root():
    try:
        updater = Updater()
        await updater.updateStar()

        return {"message": "Updated"}
    except:
        return {"message": "Update failed"}


@app.get("/")
async def root():
    return {"message": "Hello World!"}
