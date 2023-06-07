from fastapi import FastAPI
from app.ML.DataPredict import Predictor
from app.Data.Updater import Updater
import app.ML.Trainer as trainer
from app.ML.OutdoorFusionDataset import Data

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
