from app.data.Repositories.CrudRepository import Repository
import app.Tools.DbUtil as utils
import pandas as pd

# Get Data
database = 'OutdoorFusion'
repository = Repository(utils.constructConnectionString(database))

order_details = repository.findAll('Order_Details')
product = repository.findAll('Product')
customer = repository.findAll('Customer')
employee = repository.findAll('Employee')

# Merge Data
merged_data = pd.merge(order_details, product, on='PRODUCT_id')
merged_data = pd.merge(merged_data, customer, on='CUSTOMER_id')
merged_data = pd.merge(merged_data, employee, on='EMPLOYEE_id')

# Feature engineering
aggregated_data = merged_data.groupby('DAY_date').agg({
    'ORDER_DETAIL_order_quantity': 'sum',
    'PRODUCT_prod_cost': 'mean',
    'CUSTOMER_region': 'nunique',
    'EMPLOYEE_country': 'nunique'
}).reset_index()
