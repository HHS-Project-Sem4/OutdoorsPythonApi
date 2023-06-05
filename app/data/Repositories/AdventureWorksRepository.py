import pandas as pd
from app.data.Repositories.CrudRepository import Repository


class AdventureRepository(Repository):
    def __init__(self, connectionString):
        super(AdventureRepository, self).__init__(connectionString)

    def getProductDataFrame(self):
        productJoinQuery = """
        SELECT p.ProductID, p.Name, pc.Name AS CategoryName, psc.Name AS SubCategoryName, p.Color, p.StandardCost, SUM(pi.Quantity) AS Quantity
        FROM production.Product p
        FULL OUTER JOIN production.ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
        FULL OUTER JOIN production.ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
        JOIN Production.ProductInventory pi ON p.ProductID = pi.ProductID
        GROUP BY p.ProductID, p.Name, pc.Name, psc.Name, p.Color, p.StandardCost
        """

        return pd.read_sql(productJoinQuery, self.engine)

    def getCustomerDataFrame(self):
        # Distinct because of the one to many from customer -> address, only other easy way is to just exclude anything related to address

        customerJoinQuery = """
        SELECT DISTINCT c.CustomerID, a.AddressLine1, a.City, sp.Name AS StateName, cr.Name AS CountryName, s.Name AS CompanyName
        FROM sales.Customer c
        JOIN person.Person p ON c.PersonID = p.BusinessEntityID
        LEFT JOIN sales.Store s  ON c.StoreID = s.BusinessEntityID
        JOIN person.BusinessEntityAddress bea ON c.StoreID = bea.BusinessEntityID OR c.PersonID = bea.BusinessEntityID
        JOIN person.Address a ON bea.AddressID = a.AddressID
        JOIN person.StateProvince sp ON a.StateProvinceID = sp.StateProvinceID
        JOIN person.CountryRegion cr ON sp.CountryRegionCode = cr.CountryRegionCode
        """

        return pd.read_sql(customerJoinQuery, self.engine)

    def getEmployeeDataFrame(self):
        employeeJoinQuery = """
        SELECT p.BusinessEntityID, p.FirstName, p.LastName, a.City, psp.Name AS StateName, cr.Name AS CountryName
        FROM sales.SalesPerson sp
        JOIN person.Person p ON sp.BusinessEntityID = p.BusinessEntityID
        JOIN person.BusinessEntity be ON p.BusinessEntityID = be.BusinessEntityID
        JOIN person.BusinessEntityAddress bea ON p.BusinessEntityID = bea.BusinessEntityID
        JOIN person.Address a ON bea.AddressID = a.AddressID
        JOIN person.StateProvince psp ON a.StateProvinceID = psp.StateProvinceID
        JOIN person.CountryRegion cr ON psp.CountryRegionCode = cr.CountryRegionCode
        """

        return pd.read_sql(employeeJoinQuery, self.engine)

    def getDayDataFrame(self):
        return pd.read_sql("SELECT DISTINCT OrderDate FROM sales.SalesOrderHeader", self.engine)

    def getOrderDetailsDataFrame(self):
        orderDetailsQuery = """
            SELECT SalesOrderDetailID, sd.SalesOrderID, OrderQty, UnitPrice, OrderDate, sh.SalesPersonID, CustomerID, ProductID
            FROM sales.SalesOrderDetail sd
            JOIN sales.SalesOrderHeader sh ON sd.SalesOrderID = sh.SalesOrderID
        """

        data = pd.read_sql(orderDetailsQuery, self.engine)

        data[['SalesPersonID']] = data[['SalesPersonID']].fillna(-1)
        types = {'SalesPersonID': int}
        data = data.astype(types)

        return data
