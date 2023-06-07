from fastapi import FastAPI, HTTPException, BackgroundTasks

import app.ML.Trainer as trainer
from app.Data.Updater import Updater
from app.ML.DataPredict import Predictor
from app.ML.OutdoorFusionDataset import Data

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/updateStar/{confirmation}")
async def updateStar(confirmation: str, background_tasks: BackgroundTasks):
    try:
        if confirmation == 'yes':
            background_tasks.add_task(updateStarScheme)
        else:
            return {"message": "Wrong confirmation"}
    except:
        return HTTPException(status_code=400, detail="Update Failed")


async def updateStarScheme():
    # Your logic for creating the order quantity dataset
    print('Updating database...')
    updater = Updater()
    updater.updateStar()
    print('Updating complete')


# Input format below
# {
#   "Country": "UK",
#   "Product": "LL Road Pedal",
#   "Category": "Components",
#   "SubCategory": "Pedals"
# }
@app.post("/predict/unitprice")
async def getUnitPricePrediction(input: dict):
    path = 'app/Resources/Datasets/unitprice_data.pth'

    datasets = Data()
    X, Y = datasets.getUnitPriceXY()

    predictor = Predictor(path, X.columns)

    values = {
        "Country": input.get("Country"),
        "Product": input.get("Product"),
        "Category": input.get("Category"),
        "SubCategory": input.get("SubCategory")
    }
    values = datasets.getMonthValues(values)
    predictColumn  = 'Predicted_Quantity'

    predictedValue = await predictor.predict(values, predictColumn)
    returnArray = predictedValue[['DAY_MONTH_nr', predictColumn]]

    return returnArray.to_numpy()


# Input format below
# {
#     "Country": "UK",
#     "Product": "LL Road Pedal",
#     "Category": "Components",
#     "SubCategory": "Pedals"
# }
@app.post("/predict/orderquantity")
async def getOrderQuantiyPrediction(input: dict):
    path = 'app/Resources/Datasets/orderquantity_data.pth'

    datasets = Data()
    X, Y = datasets.getOrderQuantityXY()

    predictor = Predictor(path, X.columns)

    values = {
        "Country": input.get("Country"),
        "Product": input.get("Product"),
        "Category": input.get("Category"),
        "SubCategory": input.get("SubCategory")
    }

    values = datasets.getMonthValues(values)

    predictColumn = 'Predicted_Quantity'
    predictedValue = await predictor.predict(values, predictColumn)

    returnArray = predictedValue[['DAY_MONTH_nr', predictColumn]]

    return returnArray.to_numpy()


async def create_order_quantity_dataset():
    # Your logic for creating the order quantity dataset
    print('Creating order quantity dataset...')
    # Simulating a long-running task
    trainer.createOrderQuantityDataset()
    print('Order quantity dataset creation complete')


@app.post("/train/orderQuantity")
async def build_training_order_quantity(background_tasks: BackgroundTasks):
    print('TRAIN ORDER QUANTITY')

    background_tasks.add_task(create_order_quantity_dataset)

    return {"message": "Build complete"}


async def createUnitPricedataset():
    # Your logic for creating the order quantity dataset
    print('Creating unit price dataset...')
    # Simulating a long-running task
    trainer.createUnitPriceDataset()
    print('Order quantity dataset creation complete')


@app.post("/train/unitprice")
async def build_Training_Unit_Price(background_tasks: BackgroundTasks):
    print('TRAIN ORDER QUANTITY')

    background_tasks.add_task(createUnitPricedataset)

    return {"message": "Build complete"}
