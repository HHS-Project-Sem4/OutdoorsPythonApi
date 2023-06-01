import numpy as np
import pandas as pd

from app.Services.StarService import StarService
from app.Tools import utils
from app.Repositories.CrudRepository import Repository


class SalesService(StarService):

    def __init__(self, server, username, password, driver, trustedConnection):
        repository = Repository(
            self.constructConnectionString(driver, server, 'Sales_db', username, password, trustedConnection))
        super().__init__(repository)

        self.salesData = self.repository.findAll('Sales')

    def getProductDataFrame(self):
        sales = utils.addIntIDUnique(self.salesData, 'Product', 'prod_id')

        columns = ['Product', 'Product_Category', 'Sub_Category', 'Unit_Cost']

        newFrames = utils.splitFrames(sales, 'prod_id', columns)
        self.salesData = newFrames[0]
        productData = newFrames[1]

        newColumnNames = ['PRODUCT_id', 'PRODUCT_name', 'PRODUCT_category', 'PRODUCT_sub_category', 'PRODUCT_prod_cost']
        productData.columns = newColumnNames

        return productData

    def getCustomerDataFrame(self):
        # self.salesDataFrame = utils.addIntID(self.salesDataFrame, 'CUSTOMER_id')
        # newFrames = utils.splitFrames(self.salesDataFrame, 'CUSTOMER_id', ['Country', 'State'])
        #
        # self.salesDataFrame = newFrames[0]
        # customerData = newFrames[1]
        #
        # newColumnNames = ['CUSTOMER_id', 'CUSTOMER_country', 'CUSTOMER_state']
        # customerData.columns = newColumnNames
        #
        # return customerData

        return pd.DataFrame()

    def getEmployeeDataFrame(self):
        return pd.DataFrame()

    def getDayDataFrame(self):
        newFrames = utils.splitFrames(self.salesData, 'Date', [])

        self.salesData = newFrames[0]
        orderDates = newFrames[1]

        dateFormat = '%Y-%m-%d'
        DAY_date = utils.getDayDate(orderDates, 'Date', dateFormat)

        return DAY_date

    def getOrderDetailsDataFrame(self):
        orderDetailsData = self.salesData

        # create column for ids and fills it
        orderDetailsData.insert(0, 'OrderID', np.nan)
        orderDetailsData = utils.addIntID(orderDetailsData, 'OrderID')

        # selectedColumn = ['Order_Quantity', 'Unit_Price', 'Date', 'CUSTOMER_id', 'prod_id']
        selectedColumn = ['OrderID', 'Order_Quantity', 'Unit_Price', 'Date', 'prod_id']

        orderDetailsData = orderDetailsData[selectedColumn]

        # renameColumns = ['ORDER_DETAIL_order_quantity', 'ORDER_DETAIL_unit_price', 'DAY_date', 'CUSTOMER_id', 'PRODUCT_id']

        renameColumns = ['ORDER_DETAIL_id', 'ORDER_DETAIL_order_quantity', 'ORDER_DETAIL_unit_price', 'DAY_date',
                         'PRODUCT_id']

        orderDetailsData.columns = renameColumns

        return orderDetailsData
