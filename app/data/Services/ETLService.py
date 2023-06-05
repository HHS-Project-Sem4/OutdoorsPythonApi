import pandas as pd
from app.Tools import CleaningUtil as cleaningUtil
from app.data.Services.CrudService import CrudService
from app.Tools import EtlUtil
from app.data.Repositories.CrudRepository import Repository
from app.Tools import DbUtil


class ETLService(CrudService):

    def __init__(self):
        # ref used in the db config ini that contains the dbName
        dbRef = 'OutdoorFusion'

        repository = Repository(DbUtil.constructConnectionString(dbRef))

        super().__init__(repository)

    def mergeDataSets(self, dataSets):
        # create result frame
        returnSet = EtlUtil.createEmptyStarFrame()

        for dataSet in dataSets:
            print(f'ADDING: {dataSet["setName"]}')

            starToAdd = dataSet['dataService'].getStarData()
            returnSet = self.mergeDataSet(returnSet, starToAdd)

        return returnSet

    def mergeDataSet(self, base, toAdd):
        returnSet = base.copy()

        # merging consts
        factFrameName = 'Order_Details'
        factFramePrimaryKey = 'ORDER_DETAIL_id'
        factFrameNonLinkedIds = ['ORDER_HEADER_id']
        idRegex = '_id'

        returnSet = EtlUtil.mergeStarDiagrams(returnSet, toAdd, factFrameName, factFramePrimaryKey,
                                              factFrameNonLinkedIds, idRegex)

        return returnSet

    def dropAllTables(self, dbTables):
        for table in dbTables:
            self.deleteAll(table.name)

    def dropDuplicateDates(self, starFrame, dateTableName, dateIdColumnName):
        mainData = starFrame.copy()

        # drops duplicates in date table
        dateFrame = next((df for df in mainData if df.name == dateTableName), None)
        dateFrame.drop_duplicates(subset=[dateIdColumnName])

        # replaces the old Date dataframe with the clean one
        mainData = [dateFrame if df.name == dateTableName else df for df in mainData]

        return mainData

    def cleanTables(self, mainData):

        print('CHECK NULL VALS BEFORE')
        for table in mainData:
            tableName = table.name
            print(f'CHECK: {tableName}')

            EtlUtil.checkForNulls(table)

        cleanCustomerData = cleaningUtil.CleanCustomer(
            next((df for df in mainData if df.name == 'Customer'), None))
        cleanProductData = cleaningUtil.cleanProduct(
            next((df for df in mainData if df.name == 'Product'), None))
        cleanEmployeeData = cleaningUtil.cleanEmployee(
            next((df for df in mainData if df.name == 'Employee'), None))
        cleanOrderDetailsData = cleaningUtil.cleanOrderDetails(
            next((df for df in mainData if df.name == 'Order_Details'), None))
        cleanDayDate = cleaningUtil.cleanDayDate(
            next((df for df in mainData if df.name == 'Order_Date'), None))

        data = [cleanCustomerData, cleanProductData, cleanEmployeeData, cleanOrderDetailsData, cleanDayDate]

        print('CHECK NULL VALS AFTER')
        for table in data:
            tableName = table.name
            print(f'CHECK: {tableName}')

            EtlUtil.checkForNulls(table)

        return data

    def getUpdatedStar(self, dataSets):
        # creating the save frame
        print('CREATING NEW FRAME')
        mainData = EtlUtil.createEmptyStarFrame()

        self.dropAllTables(mainData)
        print('TABLES CLEARED')

        # Start the merger
        print('START MERGING')
        mainData = self.mergeDataSets(dataSets)

        print('MERGIN COMPLETE')

        EtlUtil.checkColumnForDuplicates(mainData, '_id')

        # Drop Duplicate Dates
        print('FIX DATE TABLE')
        mainData = self.dropDuplicateDates(mainData, 'Order_Date', 'DAY_date')

        mainData = self.cleanTables(mainData)
        print('TABLES CLEANED')

        return mainData

    def updateStar(self, dataSets):
        mainData = self.getUpdatedStar(dataSets)

        print('UPLOADING DATA')
        for table in mainData:
            tableName = table.name
            print(f'UPLOADING: {tableName}')

            self.saveData(table, tableName)

            print(f'UPLOADING: {tableName} | FINISHED')

        print('DONE UPLOADING TABLES')
