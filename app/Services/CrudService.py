
class CrudService:

    def __init__(self, repository):
        self.repository = repository

    def constructConnectionString(self, driver, server, dbName, username, password, trustedConnection):
        return f"DRIVER={driver};SERVER={server};DATABASE={dbName};UID={username};PWD={password};trusted_connection={trustedConnection}"

    def saveData(self, dataFrame, table):
        self.repository.saveDateFrame(dataFrame, table)

    def deleteAll(self, table):
        self.repository.dropTable(table)

    def getRepository(self):
        return self.repository