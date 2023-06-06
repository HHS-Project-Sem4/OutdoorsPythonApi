from TestDataSet import TestData
import torch

saved_data = torch.load("data.pth")

# Create mock input data
mock_data = {
    "CUSTOMER_country": [],
    "PRODUCT_name": [],
    "PRODUCT_category": [],
    "PRODUCT_sub_category": [],
    "DAY_QUARTER_nr": [],
    "DAY_MONTH_nr": [],
}

country = 'USA'
product = 'LL Road Pedal'
category = ''
subCategory = ''

for i in range(1, 13):
    q = (i - 1) // 3 + 1

    mock_data["CUSTOMER_country"].append(country)
    mock_data["PRODUCT_name"].append(product)
    mock_data["PRODUCT_category"].append(category)
    mock_data["PRODUCT_sub_category"].append(subCategory)
    mock_data["DAY_MONTH_nr"].append(i)
    mock_data["DAY_QUARTER_nr"].append(q)

testData = TestData(saved_data)
result_df = testData.predict(mock_data)

usedColumns = ['CUSTOMER_country', 'PRODUCT_name', 'PRODUCT_category', 'PRODUCT_sub_category', 'DAY_QUARTER_nr',
               'DAY_MONTH_nr', 'Predicted_price']

r2 = result_df[usedColumns]

# Print the result
print('R2')
print(r2)