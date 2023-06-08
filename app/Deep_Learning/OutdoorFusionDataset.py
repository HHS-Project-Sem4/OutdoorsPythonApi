from app.Data.Repositories.CrudRepository import Repository
from app.Tools import DbUtil as dbUtil
import pandas as pd


class Data:

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

    def getDataXY(self, yColumn, allColumns):
        # Select relevant columns
        selectedColumns = allColumns

        selectedData = self.mergedData[selectedColumns]
        selectedData = selectedData.dropna()

        encodedData = self.encodeData(selectedData)

        X = encodedData.drop(yColumn, axis=1)
        Y = encodedData[yColumn]

        return X, Y

    def getOrderQuantityXY(self):
        # Select relevant columns
        selectedColumns = ['CUSTOMER_country', 'PRODUCT_name', 'PRODUCT_category', 'PRODUCT_sub_category',
                           'ORDER_DETAIL_order_quantity',
                           'DAY_QUARTER_nr', 'DAY_MONTH_nr']

        yColumn = 'ORDER_DETAIL_order_quantity'

        return self.getDataXY(yColumn, selectedColumns)

    def getUnitPriceXY(self):
        # Select relevant columns
        selectedColumns = ['CUSTOMER_country', 'PRODUCT_name', 'PRODUCT_category', 'PRODUCT_sub_category',
                           'ORDER_DETAIL_unit_price', 'DAY_QUARTER_nr', 'DAY_MONTH_nr']

        yColumn = 'ORDER_DETAIL_unit_price'

        return self.getDataXY(yColumn, selectedColumns)

    def encodeData(self, data):
        # Encode date into numeric values
        typeFix = {'DAY_QUARTER_nr': 'string', 'DAY_MONTH_nr': 'string'}
        selectedData = data.astype(typeFix)

        encodedData = pd.get_dummies(selectedData)

        return encodedData

    def getMonthValues(self, inputValues):
        country = inputValues['Country']
        product = inputValues['Product']
        category = inputValues['Category']
        subCategory = inputValues['SubCategory']

        mock_data = {
            "CUSTOMER_country": [],
            "PRODUCT_name": [],
            "PRODUCT_category": [],
            "PRODUCT_sub_category": [],
            "DAY_QUARTER_nr": [],
            "DAY_MONTH_nr": [],
        }

        for i in range(1, 13):
            q = (i - 1) // 3 + 1

            mock_data["CUSTOMER_country"].append(country)
            mock_data["PRODUCT_name"].append(product)
            mock_data["PRODUCT_category"].append(category)
            mock_data["PRODUCT_sub_category"].append(subCategory)
            mock_data["DAY_MONTH_nr"].append(i)
            mock_data["DAY_QUARTER_nr"].append(q)

        return mock_data
