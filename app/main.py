import sys
sys.path.append('./')

from fastapi import FastAPI
from ML.DataPredict import Predictor
from data.Updater import Updater
import ML.Trainer as trainer
from ML.OutdoorFusionDataset import Data

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/updateStar")
async def root():
    try:
        updater = Updater()
        await updater.updateStar()

        return {"message": "Updated"}
    except:
        return {"message": "Update failed"}


# Input format below
# inputValues = {
#     'Country' : 'UK',
#     'Product' : 'LL Road Pedal',
#     'Category' : 'Components',
#     'SubCategory' : 'Pedals',
# }
@app.get("/predict/unitprice")
async def getUnitPricePrediction(inputValues):
    path = 'unitprice_data.pth'

    datasets = Data()
    X, Y = datasets.getOrderQuantityXY()

    predictor = Predictor(path, X.columns)

    values = datasets.getMonthValues(inputValues)
    predictedValue = predictor.predict(values, 'Predicted_Price')

    return predictedValue


# Input format below
# inputValues = {
#     'Country' : 'UK',
#     'Product' : 'LL Road Pedal',
#     'Category' : 'Components',
#     'SubCategory' : 'Pedals',
# }
@app.get("/predict/orderquantity")
async def getOrderQuantiyPrediction(inputValues):
    path = 'orderquantity_data.pth'

    datasets = Data()
    X, Y = datasets.getOrderQuantityXY()

    predictor = Predictor(path, X.columns)

    values = datasets.getMonthValues(inputValues)
    predictedValue = predictor.predict(values, 'Predicted_Quantity')

    return predictedValue


@app.get("/train/orderquantity")
async def buildTrainingOrderQuantity():
    trainer.createOrderQuantityDataset()


@app.get("/train/unitprice")
async def buildTrainingUnitPrice():
    trainer.createUnitPriceDataset()
