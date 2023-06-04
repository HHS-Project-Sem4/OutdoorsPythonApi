from app.Services.AbstractStarService import StarService
from app.Repositories.AdventureWorksRepository import AdventureRepository
from app.Tools import DbUtil, EtlUtil


class AdventureWorksService(StarService):

    def __init__(self):
        # ref used in the db config ini that contains the dbName
        dbRef = 'AdventureWorks'
        repository = AdventureRepository(DbUtil.constructConnectionString(dbRef))

        super().__init__(repository)

    def getProductDataFrame(self):
        productData = self.repository.getProductDataFrame()

        renameColumns = ['PRODUCT_id', 'PRODUCT_name', 'PRODUCT_category', 'PRODUCT_sub_category', 'PRODUCT_colour',
                         'PRODUCT_prod_cost', 'PRODUCT_storage_quantity']
        productData.columns = renameColumns

        return productData

    def getCustomerDataFrame(self):
        customerData = self.repository.getCustomerDataFrame()

        renameColumns = ['CUSTOMER_id', 'CUSTOMER_address', 'CUSTOMER_city', 'CUSTOMER_state', 'CUSTOMER_country',
                         'CUSTOMER_company_name']
        customerData.columns = renameColumns

        customerData.drop_duplicates(subset=['CUSTOMER_id'], keep="first", inplace=True)

        return customerData

    def getEmployeeDataFrame(self):
        employeeData = self.repository.getEmployeeDataFrame()

        # Rename columns
        renameColumns = ['EMPLOYEE_id', 'EMPLOYEE_first_name', 'EMPLOYEE_last_name', 'EMPLOYEE_city', 'EMPLOYEE_state',
                         'EMPLOYEE_country']

        employeeData.columns = renameColumns

        return employeeData

    def getDayDataFrame(self):
        orderDates = self.repository.getDayDataFrame()

        dateFormat = '%Y-%m-%d'
        DAY_date = EtlUtil.createDayDateDataframe(orderDates, 'OrderDate', dateFormat)

        return DAY_date

    def getOrderDetailsDataFrame(self):
        orderDetailsData = self.repository.getOrderDetailsDataFrame()

        renameColumns = ['ORDER_DETAIL_id', 'ORDER_HEADER_id', 'ORDER_DETAIL_order_quantity', 'ORDER_DETAIL_unit_price',
                         'DAY_date',
                         'EMPLOYEE_id', 'CUSTOMER_id', 'PRODUCT_id']

        orderDetailsData.columns = renameColumns

        return orderDetailsData

