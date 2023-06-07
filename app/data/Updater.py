import sys
sys.path.append('../')

from data.Services.AENCService import AENCService
from data.Services.AdventureWorksService import AdventureWorksService
from data.Services.ETLService import ETLService
from data.Services.NorthwindService import NorthwindService
from data.Services.SalesService import SalesService


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