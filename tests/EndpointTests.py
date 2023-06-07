from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def testBuildTrainingOrderQuantity():
    response = client.get("/train/orderquantity")
    assert response.status_code == 200
    assert response.json() == {"message": "Order quantity training dataset created successfully"}


def testBuildTrainingUnitPrice():
    response = client.get("/train/unitprice")
    assert response.status_code == 200
    assert response.json() == {"message": "Order quantity training dataset created successfully"}
