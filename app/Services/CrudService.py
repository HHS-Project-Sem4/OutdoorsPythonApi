
class CrudService:

    def __init__(self, repository):
        self.repository = repository


    def saveData(self, dataFrame, table):
        self.repository.saveDateFrame(dataFrame, table)

    def deleteAll(self, table):
        self.repository.dropTable(table)

    def getRepository(self):
        return self.repository