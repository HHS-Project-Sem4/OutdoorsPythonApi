from app.Tools import CleaningUtil as cleaningUtil
from app.Tools import DbUtil
from app.Tools import EtlUtil
from app.Data.Repositories.CrudRepository import Repository
from app.Data.Services.CrudService import CrudService


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
        cleaning_functions = {
            'Customer': cleaningUtil.CleanCustomer,
            'Product': cleaningUtil.cleanProduct,
            'Employee': cleaningUtil.cleanEmployee,
            'Order_Details': cleaningUtil.cleanOrderDetails,
            'Order_Date': cleaningUtil.cleanDayDate
        }

        data = []

        print('CHECK NULL VALS BEFORE')
        for table in mainData:

            tableName = table.name
            print(f'CHECK: {tableName}')
            EtlUtil.checkForNulls(table)

            if tableName in cleaning_functions:
                cleaning_function = cleaning_functions[tableName]
                cleaned_table = cleaning_function(table)
                data.append(cleaned_table)

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
