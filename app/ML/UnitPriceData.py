from app.data.Repositories.CrudRepository import Repository
from app.Tools import DbUtil as dbUtil
import pandas as pd
import torch


class Data:

    def getXYTensor(self):
        # Get data
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

        # Select relevant columns
        selectedColumns = ['CUSTOMER_country', 'PRODUCT_name', 'PRODUCT_category', 'PRODUCT_sub_category',
                           'ORDER_DETAIL_unit_price', 'DAY_QUARTER_nr', 'DAY_MONTH_nr']
        selectedData = mergedData[selectedColumns]

        selectedData = selectedData.dropna()

        # Encode date into numeric values
        typeFix = {'DAY_QUARTER_nr': 'string', 'DAY_MONTH_nr': 'string'}
        selectedData = selectedData.astype(typeFix)

        encodedData = pd.get_dummies(selectedData)

        X = encodedData.drop('ORDER_DETAIL_unit_price', axis=1)
        Y = encodedData['ORDER_DETAIL_unit_price']

        return X, Y
