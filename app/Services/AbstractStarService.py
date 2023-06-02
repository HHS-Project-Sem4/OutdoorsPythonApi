from abc import abstractmethod

from app.Services.CrudService import CrudService


# idk how abstract classes work in python tbh
class StarService(CrudService):

    def __init__(self, repository):
        super().__init__(repository)

    @abstractmethod
    def getProductDataFrame(self):
        pass

    @abstractmethod
    def getCustomerDataFrame(self):
        pass

    @abstractmethod
    def getEmployeeDataFrame(self):
        pass

    @abstractmethod
    def getDayDataFrame(self):
        pass

    @abstractmethod
    def getOrderDetailsDataFrame(self):
        pass

    def getStarData(self):
        product_df = self.getProductDataFrame()
        customer_df = self.getCustomerDataFrame()
        employee_df = self.getEmployeeDataFrame()
        day_df = self.getDayDataFrame()
        order_details_df = self.getOrderDetailsDataFrame()

        product_df.name = 'Product'
        customer_df.name = 'Customer'
        employee_df.name = 'Employee'
        day_df.name = 'Order_Date'
        order_details_df.name = 'Order_Details'

        data = [product_df, customer_df, employee_df, day_df, order_details_df]

        return data
