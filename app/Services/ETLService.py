from app.Services.CrudService import CrudService
from app.Repositories.CrudRepository import Repository
from app.Tools import utils


class ETLService(CrudService):

    def __init__(self, server, username, password, driver, trustedConnection):
        repository = Repository(
            utils.constructConnectionString(driver, server, 'OutdoorFusion', username, password, trustedConnection))

        super().__init__(repository)

    def mergeDataSets(self, dataSets):
        # create result frame
        returnSet = utils.createEmptyStarFrame()

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
        idRegex = '_id'

        base = utils.mergeStarDiagrams(base, toAdd, factFrameName, factFramePrimaryKey, idRegex)

        return base

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

    def getCompleteUpdateStar(self, dataSets):
        # creating the save frame
        print('CREATING NEW FRAME')
        mainData = utils.createEmptyStarFrame()

        self.dropAllTables(mainData)
        print('TABLES CLEANED')

        # Start the merger
        print('START MERGING')
        mainData = self.mergeDataSets(dataSets)

        print('MERGIN COMPLETE')

        utils.dupC(mainData)

        # Drop Duplicate Dates
        print('FIX DATE TABLE')
        mainData = self.dropDuplicateDates(mainData, 'Order_Date', 'DAY_date')

        return mainData

    def completeUpdateStar(self, dataSets):
        mainData = self.getCompleteUpdateStar(dataSets)

        # Make the uploading use virtual threads to increase the speed
        print('UPLOADING DATA')
        for table in mainData:
            tableName = table.name
            print(f'UPLOADING: {tableName}')

            for column in table.columns:
                if '_id' in column:
                    # have to cast to string first otherwise get: Cannot cast array data from dtype('O') to dtype('int32') according to the rule 'safe'

                    types = {column: 'string'}
                    table = table.astype(types)

                    types = {column: 'Int32'}
                    table = table.astype(types)

            self.saveData(table, tableName)

            print(f'UPLOADING: {tableName} | FINISHED')

        print('DONE UPLOADING TABLES')