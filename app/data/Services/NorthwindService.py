import sys
sys.path.append('../../')

import pandas as pd

from data.Services.AbstractStarService import StarService
from data.Repositories.NorthwindRepository import NorthwindRepository
from Tools import DbUtil, EtlUtil


class NorthwindService(StarService):

    def __init__(self):
        # ref used in the db config ini that contains the dbName
        dbRef = 'Northwind'

        repository = NorthwindRepository(DbUtil.constructConnectionString(dbRef))

        super().__init__(repository)

    def getProductDataFrame(self):
        productData = self.repository.getProductDataFrame()

        newColumnNames = ['PRODUCT_id', 'PRODUCT_name', 'PRODUCT_sub_category']
        productData.columns = newColumnNames

        productData['PRODUCT_category'] = 'Foodstuff'

        return productData

    def getCustomerDataFrame(self):
        customerData = self.repository.getCustomerDataFrame()

        newColumnNames = ['CUSTOMER_id', 'CUSTOMER_address', 'CUSTOMER_city', 'CUSTOMER_country',
                          'CUSTOMER_company_name']
        customerData.columns = newColumnNames

        return customerData

    def getEmployeeDataFrame(self):
        employeeData = self.repository.getEmployeeDataFrame()

        newColumnNames = ['EMPLOYEE_id', 'EMPLOYEE_first_name', 'EMPLOYEE_city', 'EMPLOYEE_country']
        employeeData.columns = newColumnNames

        return employeeData

    def getDayDataFrame(self):
        orderDates = self.repository.getDayDataFrame()

        dateFormat = '%Y-%m-%d'
        DAY_date = EtlUtil.createDayDateDataframe(orderDates, 'OrderDate', dateFormat)

        return DAY_date

    def getOrderDetailsDataFrame(self):
        orderDetailsData = self.repository.getOrderDetailsDataFrame()

        orderDetailsData = EtlUtil.addIntID(orderDetailsData, 'OrderID')

        renameColumns = ['ORDER_DETAIL_id',
                         'ORDER_HEADER_id', 'ORDER_DETAIL_order_quantity', 'ORDER_DETAIL_unit_price', 'DAY_date',
                         'EMPLOYEE_id', 'CUSTOMER_id', 'PRODUCT_id']
        orderDetailsData.columns = renameColumns

        dateFormat = '%Y-%m-%d'
        orderDetailsData['DAY_date'] = pd.to_datetime(orderDetailsData['DAY_date'], format=dateFormat)

        return orderDetailsData
