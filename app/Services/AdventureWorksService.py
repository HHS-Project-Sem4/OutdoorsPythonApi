from app.Services.StarService import StarService
from app.Tools import utils
from app.Repositories.AdventureWorksRepository import AdventureRepository


class AdventureWorksService(StarService):

    def __init__(self, server, username, password, driver, trustedConnection):
        repository = AdventureRepository(
            self.constructConnectionString(driver, server, 'AdventureWorks', username, password, trustedConnection))

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

        # dropping duplicates on this column because of the one to many relationship with businessentity and businessEntityAddress, only other way is to just exclude the address etc data
        customerData.drop_duplicates(subset=['CUSTOMER_id'])

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
        DAY_date = utils.getDayDate(orderDates, 'OrderDate', dateFormat)

        return DAY_date

    def getOrderDetailsDataFrame(self):
        orderDetailsData = self.repository.getOrderDetailsDataFrame()

        renameColumns = ['ORDER_DETAIL_id', 'ORDER_HEADER_id', 'ORDER_DETAIL_order_quantity', 'ORDER_DETAIL_unit_price',
                         'DAY_date',
                         'EMPLOYEE_id', 'CUSTOMER_id', 'PRODUCT_id']

        orderDetailsData.columns = renameColumns

        return orderDetailsData

