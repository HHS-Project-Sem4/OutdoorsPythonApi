from app.Services.AENCService import AENCService
from app.Services.AdventureWorksService import AdventureWorksService
from app.Services.ETLService import ETLService
from app.Services.NorthwindService import NorthwindService
from app.Services.SalesService import SalesService


class Updater:

    async def updateStar(self):
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
