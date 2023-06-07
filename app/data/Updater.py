from app.Data.Services.AENCService import AENCService
from app.Data.Services.AdventureWorksService import AdventureWorksService
from app.Data.Services.ETLService import ETLService
from app.Data.Services.NorthwindService import NorthwindService
from app.Data.Services.SalesService import SalesService


class Updater:

    def updateStar(self):
        etlService = ETLService()

        northWindService = NorthwindService()
        aencService = AENCService()
        adventureWorksService = AdventureWorksService()
        salesService = SalesService()

        dataSets = [
            {'setName': 'Northwind', 'dataService': northWindService},
            {'setName': 'AENC', 'dataService': aencService},
            {'setName': 'AdventureWorks', 'dataService': adventureWorksService},
            {'setName': 'Sales_db', 'dataService': salesService}
        ]

        etlService.updateStar(dataSets)


u = Updater()

u.updateStar()