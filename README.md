# OutdoorsPythonApi

## Endpoints
/updateStar/{confirmation}"
Used to update the star scheme, needs confirmation just in case.

/predict/unitprice
predicts unit value for 12 months based on the json body it gets
body should look like the following
{
    "Country": "",
    "Product": "",
    "Category": "",
    "SubCategory": ""
}
response will look like the following
{
  "1.0": 22.525678634643555,
  "2.0": 22.525678634643555,
  "3.0": 22.525678634643555,
  "4.0": 22.525678634643555,
  "5.0": 22.525678634643555,
  "6.0": 22.525678634643555,
  "7.0": 22.525678634643555,
  "8.0": 22.525678634643555,
  "9.0": 22.525678634643555,
  "10.0": 22.525678634643555,
  "11.0": 22.525678634643555,
  "12.0": 22.525678634643555
}

/predict/orderquantity
predicts order quantity for 12 months based on the json body it gets
body should look like the following
{
    "Country": "",
    "Product": "",
    "Category": "",
    "SubCategory": ""
}
response will look like the following
{
  "1.0": 2.5693163871765137,
  "2.0": 2.5693163871765137,
  "3.0": 2.5693163871765137,
  "4.0": 2.5693163871765137,
  "5.0": 6.752440929412842,
  "6.0": 2.5693163871765137,
  "7.0": 6.7899065017700195,
  "8.0": 2.5693163871765137,
  "9.0": 2.5693163871765137,
  "10.0": 5.005955696105957,
  "11.0": 2.5693163871765137,
  "12.0": 2.5693163871765137
}

/train/orderQuantity
trains the model used by the endpoint that predicts the order quantity

/train/unitprice
trains the model used by the endpoint that predicts the unit price
