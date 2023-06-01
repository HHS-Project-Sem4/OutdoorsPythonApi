from Services.ETLService import ETLService
from Services.AENCService import AENCService
from Services.AdventureWorksService import AdventureWorksService
from Services.SalesService import SalesService
from Services.NorthwindService import NorthwindService

class test:

    def updateStar(self):
        server = 'DESKTOP-8INVJ1O\SQLEXPRESS'
        username = 'DESKTOP-8INVJ1O\Max'
        password = ''
        driver = '{ODBC Driver 17 for SQL Server}'
        trustedConnection = 'yes'

        etlService = ETLService(server, username, password, driver, trustedConnection)

        northWindService = NorthwindService(server, username, password, driver, trustedConnection)
        aencService = AENCService(server, username, password, driver, trustedConnection)
        adventureWorksService = AdventureWorksService(server, username, password, driver, trustedConnection)
        salesService = SalesService(server, username, password, driver, trustedConnection)

        dataSets = [
            {'setName': 'Northwind', 'dataService': northWindService},
            {'setName': 'AENC', 'dataService': aencService},
            {'setName': 'AdventureWorks', 'dataService': adventureWorksService},
            {'setName': 'Sales_db', 'dataService': salesService}
        ]

        etlService.completeUpdateStar(dataSets)
