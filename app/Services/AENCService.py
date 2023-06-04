from app.Services.AbstractStarService import StarService
from app.Tools import EtlUtil
from app.Repositories.AENCRepository import AENCRepository
from app.Tools import DbUtil

class AENCService(StarService):

    def __init__(self):
        # ref used in the db config ini that contains the dbName
        dbRef = 'AENC'
        repository = AENCRepository(DbUtil.constructConnectionString(dbRef))

        super().__init__(repository)

    def getProductDataFrame(self):
        productData = self.repository.getProductDataFrame()

        newColumnNames = ['PRODUCT_id', 'PRODUCT_name', 'PRODUCT_sub_category', 'PRODUCT_category', 'PRODUCT_colour',
                          'PRODUCT_storage_quantity']
        productData.columns = newColumnNames

        return productData

    def getCustomerDataFrame(self):
        customerData = self.repository.getCustomerDataFrame()

        newColumnNames = ['CUSTOMER_id', 'CUSTOMER_address', 'CUSTOMER_city', 'CUSTOMER_state', 'CUSTOMER_region',
                          'CUSTOMER_country', 'CUSTOMER_company_name']
        customerData.columns = newColumnNames

        return customerData

    def getEmployeeDataFrame(self):
        employeeData = self.repository.getEmployeeDataFrame()

        newColumnNames = ['EMPLOYEE_id', 'EMPLOYEE_first_name', 'EMPLOYEE_last_name', 'EMPLOYEE_city']
        employeeData.columns = newColumnNames

        return employeeData

    def getDayDataFrame(self):
        orderDates = self.repository.getDayDataFrame()

        # az db
        dateFormat = '%Y-%m-%d %H:%M:%S.%f'

        # pv db
        # dateFormat = '%d-%b-%Y %H:%M:%S %p'

        DAY_date = EtlUtil.createDayDateDataframe(orderDates, 'order_date', dateFormat)

        return DAY_date

    def getOrderDetailsDataFrame(self):
        orderDetailsData = self.repository.getOrderDetailsDataFrame()

        orderDetailsData = EtlUtil.addIntID(orderDetailsData, 'OrderDetailID')

        renameColumns = ['ORDER_DETAIL_id', 'ORDER_HEADER_id', 'CUSTOMER_id', 'DAY_date', 'EMPLOYEE_id', 'PRODUCT_id',
                         'ORDER_DETAIL_unit_price', 'ORDER_DETAIL_order_quantity']
        orderDetailsData.columns = renameColumns

        return orderDetailsData
