from fastapi import FastAPI, HTTPException
from app.ML.DataPredict import Predictor
from app.Data.Updater import Updater
import app.ML.Trainer as trainer
from app.ML.OutdoorFusionDataset import Data

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World3"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/updateStar/{confirmation}")
async def updateStar(confirmation: str):
    try:
        if confirmation == 'yes':
            updater = Updater()
            await updater.updateStar()

            return {"message": "Updated"}
        else:
            return {"message": "Wrong confirmation"}
    except:
        return HTTPException(status_code=400, detail="Update Failed")


# Input format below
# {
#   "Country": "UK",
#   "Product": "LL Road Pedal",
#   "Category": "Components",
#   "SubCategory": "Pedals"
# }
@app.post("/predict/unitprice")
async def getUnitPricePrediction(input: dict):
    path = 'app/ML/unitprice_data.pth'

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
    predictedValue = predictor.predict(values, 'Predicted_Price')

    return predictedValue.to_json(orient='records', index=False)


# Input format below
# {
#   "Country": "UK",
#   "Product": "LL Road Pedal",
#   "Category": "Components",
#   "SubCategory": "Pedals"
# }
@app.post("/predict/orderquantity")
async def getOrderQuantiyPrediction(input: dict):
    print(input)

    path = 'app/ML/orderquantity_data.pth'

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
    predictedValue = predictor.predict(values, 'Predicted_Quantity')

    return predictedValue.to_json(orient='records' , index=False)


@app.post("/train/orderquantity")
async def buildTrainingOrderQuantity():
    print('TRAIN ORDER QUANTITY')

    trainer.createOrderQuantityDataset()


@app.post("/train/unitprice")
async def buildTrainingUnitPrice():
    print('TRAIN UNIT PRICE')

    trainer.createUnitPriceDataset()
