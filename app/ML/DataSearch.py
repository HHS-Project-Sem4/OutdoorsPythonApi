import pandas as pd
import DbUtil
import CrudRepository

# Get data
connectionString = DbUtil.constructConnectionString('OutdoorFusion')
dataRepository = CrudRepository.findAll(connectionString, 'Order_Details')

order_details = CrudRepository.findAll(connectionString, 'Order_Details')
product = CrudRepository.findAll(connectionString, 'Product')
customer = CrudRepository.findAll(connectionString, 'Customer')
employee = CrudRepository.findAll(connectionString, 'Employee')
dayDate = CrudRepository.findAll(connectionString, 'Order_Date')

mergedData = pd.merge(order_details, product, on='PRODUCT_id')
mergedData = pd.merge(mergedData, customer, on='CUSTOMER_id')

column = 'PRODUCT_name'
product = 'LL Road Pedal'

filtered_data = mergedData[mergedData['PRODUCT_name'] == 'LL Road Pedal']

selectColumns = ['CUSTOMER_country','PRODUCT_name','PRODUCT_category','PRODUCT_sub_category','ORDER_DETAIL_unit_price']
selectedData = filtered_data[selectColumns]