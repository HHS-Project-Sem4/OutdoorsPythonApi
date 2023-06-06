from app.data.Repositories.CrudRepository import Repository
from app.Tools import DbUtil as dbUtil
import pandas as pd
import torch

connectionString = dbUtil.constructConnectionString('OutdoorFusion')
dataRepository = Repository(connectionString)

order_details = dataRepository.findAll('Order_Details')
product = dataRepository.findAll('Product')
customer = dataRepository.findAll('Customer')
employee = dataRepository.findAll('Employee')
dayDate = dataRepository.findAll('Order_Date')

mergedData = pd.merge(order_details, product, on='PRODUCT_id')
mergedData = pd.merge(mergedData, customer, on='CUSTOMER_id')

column = 'PRODUCT_name'
product = 'LL Road Pedal'

filtered_data = mergedData[mergedData['PRODUCT_name'] == 'LL Road Pedal']

selectColumns = ['CUSTOMER_country','PRODUCT_name','PRODUCT_category','PRODUCT_sub_category','ORDER_DETAIL_unit_price']
selectedData = filtered_data[selectColumns]