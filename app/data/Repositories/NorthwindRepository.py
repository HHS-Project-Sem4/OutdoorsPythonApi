import sys
sys.path.append('../../')

import pandas as pd
from data.Repositories.CrudRepository import Repository


class NorthwindRepository(Repository):

    def __init__(self, connectionString):
        super(NorthwindRepository, self).__init__(connectionString)

    # can add a category on top as food/drinks etc?
    def getProductDataFrame(self):
        productJoinQuery = """
        SELECT ProductID, ProductName, CategoryName
        FROM products p 
        JOIN Categories c ON p.CategoryID = c.CategoryID
        """

        return pd.read_sql(productJoinQuery, self.engine)

    def getCustomerDataFrame(self):
        customerJoinQuery = """
        SELECT CustomerID, Address, City, Country, CompanyName
        FROM customers
        """
        return pd.read_sql(customerJoinQuery, self.engine)

    def getEmployeeDataFrame(self):
        employeeJoinQuery = """
        SELECT EmployeeID, FirstName, City, Country
        FROM employees
        """

        return pd.read_sql(employeeJoinQuery, self.engine)

    def getDayDataFrame(self):
        return pd.read_sql("SELECT DISTINCT OrderDate FROM orders", self.engine)

    def getOrderDetailsDataFrame(self):
        orderDetailsQuery = """
        SELECT null AS OrderID ,o.OrderID AS OrderHeaderID ,Quantity, UnitPrice, OrderDate, EmployeeID, CustomerID, ProductID
        FROM [order details] od
        JOIN orders o ON od.OrderID = o.OrderID
        """

        return pd.read_sql(orderDetailsQuery, self.engine)
