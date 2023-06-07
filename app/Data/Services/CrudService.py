class CrudService:

    def __init__(self, repository):
        self.repository = repository

    def saveData(self, dataFrame, table):
        print('NO SAVE')
        # self.repository.saveDateFrame(dataFrame, table)

    def deleteAll(self, table):
        try:
            print('NO DELETE')
            # self.repository.dropTable(table)
        except:
            print('Something went wrong while dropping table, either table is not present or something else')

    def getRepository(self):
        return self.repository
