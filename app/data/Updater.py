from app.data.Services.AENCService import AENCService
from app.data.Services.AdventureWorksService import AdventureWorksService
from app.data.Services.ETLService import ETLService
from app.data.Services.NorthwindService import NorthwindService
from app.data.Services.SalesService import SalesService


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
