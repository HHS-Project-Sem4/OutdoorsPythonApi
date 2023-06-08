import pandas as pd

from app.Data.Repositories.CrudRepository import Repository
from app.Tools import DbUtil as dbUtil


class AnalyzerBase:

    def __init__(self):
        connectionString = dbUtil.constructConnectionString('OutdoorFusion')
        dataRepository = Repository(connectionString)

        order_details = dataRepository.findAll('Order_Details')
        product = dataRepository.findAll('Product')
        customer = dataRepository.findAll('Customer')
        employee = dataRepository.findAll('Employee')
        dayDate = dataRepository.findAll('Order_Date')

        # Merge Data
        mergedData = pd.merge(order_details, product, on='PRODUCT_id')
        mergedData = pd.merge(mergedData, customer, on='CUSTOMER_id')
        mergedData = pd.merge(mergedData, employee, on='EMPLOYEE_id')
        mergedData = pd.merge(mergedData, dayDate, on='DAY_date')

        self.mergedData = mergedData
