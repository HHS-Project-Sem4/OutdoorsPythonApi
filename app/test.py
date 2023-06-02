from app.Services.AENCService import AENCService
from app.Services.AdventureWorksService import AdventureWorksService
from app.Services.ETLService import ETLService
from app.Services.NorthwindService import NorthwindService
from app.Services.SalesService import SalesService
from app.Repositories.CrudRepository import Repository
from app.Repositories.AENCRepository import AENCRepository
from app.Tools import utils
class test:

    def updateStar(self):
        server = 'outdoorfusionserver.database.windows.net'
        username = 'floep'
        password = 'WaaromWilDePausNietGecremeerdWorden?HijLeeftNog'
        driver = '{ODBC Driver 17 for SQL Server}'
        trustedConnection = 'no'

        etlService = ETLService(server, username, password, driver, trustedConnection)

        northWindService = NorthwindService(server, username, password, driver, trustedConnection)
        aencService = AENCService(server, username, password, driver, trustedConnection)
        adventureWorksService = AdventureWorksService(server, username, password, driver, trustedConnection)
        salesService = SalesService(server, username, password, driver, trustedConnection)

        nStar = northWindService.getStarData()
        aencStar = aencService.getStarData()
        adventureStar = adventureWorksService.getStarData()
        salesStar = salesService.getStarData()

        # dataSets = [
        #     {'setName': 'Northwind', 'dataService': northWindService},
        #     {'setName': 'AENC', 'dataService': aencService},
        #     {'setName': 'AdventureWorks', 'dataService': adventureWorksService},
        #     {'setName': 'Sales_db', 'dataService': salesService}
        # ]

        # dataSets = [
        #     {'setName': 'Northwind', 'dataService': northWindService},
        #     {'setName': 'AENC', 'dataService': aencService},
        # ]
        #
        # etlService.completeUpdateStar(dataSets)
