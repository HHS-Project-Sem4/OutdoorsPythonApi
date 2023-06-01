import Merging.Tools.utils as utils
from Merging.Repositories.AENCRepository import AENCRepository as aencRepository
from Merging.Repositories.NorthwindRepository import NorthwindRepository as northwindRepository
from Merging.Repositories.AdventureWorksRepository import AdventureRepository as adventureWorksRepository
from Merging.Repositories.SalesRepository import SalesRepository as salesRepository
from Merging.Repositories.Repository import Repository as repository

class BrightSpaceData:

    def __init__(self, server, username, password, driver):
        self.server = server
        self.username = username
        self.password = password
        self.driver = driver

    def constructConnectionString(self, dbName):
        return f"DRIVER={self.driver};SERVER={self.server};DATABASE={dbName};UID={self.username};PWD={self.password};"

    def getStarData(self, repository, dbName):
        connectionString = self.constructConnectionString(dbName)
        print(f'CONNECTION: {connectionString}')

        repository = repository(connectionString)

        product_df = repository.getProductDataFrame()
        customer_df = repository.getCustomerDataFrame()
        employee_df = repository.getEmployeeDataFrame()
        day_df = repository.getDayDataFrame()
        order_details_df = repository.getOrderDetailsDataFrame()

        product_df.name = 'Product'
        customer_df.name = 'Customer'
        employee_df.name = 'Employee'
        day_df.name = 'Order_Date'
        order_details_df.name = 'Order_Details'

        data = [product_df, customer_df, employee_df, day_df, order_details_df]

        return data

    def saveData(self, repository, dbName, dataFrame, table):
        connectionString = self.constructConnectionString(dbName)
        repository = repository(connectionString)

        repository.saveData(dataFrame, table)

    def updateData(self, repository, outputDbName, dataframesToUpdate):
        for table in dataframesToUpdate:
            self.saveData(repository, outputDbName, dataframesToUpdate[table], table)

    def dropTableData(self, repository, dbName, tableName):
        connectionString = self.constructConnectionString(dbName)

        repository = repository(connectionString)
        repository.dropTable(tableName)

    def completeUpdateStar(self, outputDb):
        # creating the save frame
        completeStar = utils.createEmptyStarFrame()

        for table in completeStar:
            self.dropTableData(repository, outputDb, table.name)

        # getting the data
        dataSets = [
            ['Northwind', northwindRepository],
            ['AENC', aencRepository],
            ['AdventureWorks', adventureWorksRepository],
            ['Sales_db', salesRepository]
        ]

        # merging consts
        factFrameName = 'Order_Details'
        factFramePrimaryKey = 'ORDER_DETAIL_id'
        idRegex = '_id'

        for dataSet in dataSets:
            print(f'ADDING: {dataSet[0]}')
            starToAdd = self.getStarData(dataSet[1], dataSet[0])
            completeStar = utils.mergeStarDiagrams(completeStar, starToAdd, factFrameName, factFramePrimaryKey, idRegex)

        # Check for duplicates, duplicates in adventureworks CUSTOMER_id are immortal and wont even die when using DISTINCT or drop_duplicates
        utils.dupC(completeStar)

        print('FIXING DATA')
        # dropping duplicate dates added during merge
        dateFrame = next((df for df in completeStar if df.name == 'Order_Date'), None)
        dateFrame.drop_duplicates(subset=['DAY_date'])
        mainData = [dateFrame if df.name == 'Order_Date' else df for df in completeStar]

        # Make the uploading use virtual threads to increase the speed
        print('UPLOADING DATA')
        for table in mainData:
            print(f'UPLOADING: {table.name}')
            self.saveData(repository, outputDb, table, table.name)
