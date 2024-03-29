import pandas as pd
from app.Data.Repositories.CrudRepository import Repository


class AENCRepository(Repository):
    def __init__(self, connectionString):
        super(AENCRepository, self).__init__(connectionString)

    def getProductDataFrame(self):
        productJoinQuery = """
        SELECT id, description, name, category, color, quantity
        FROM product
        """

        return pd.read_sql(productJoinQuery, self.engine)

    def getCustomerDataFrame(self):
        customerJoinQuery = """
        SELECT id, address, city, state_name, region, country, company_name
        FROM customer c
        JOIN state s ON c.state = s.state_id
        """

        return pd.read_sql(customerJoinQuery, self.engine)

    def getEmployeeDataFrame(self):
        employeeJoinQuery = """
        SELECT emp_id, emp_fname, emp_lname, city
        FROM employee
        """

        return pd.read_sql(employeeJoinQuery, self.engine)

    def getDayDataFrame(self):
        return pd.read_sql("SELECT DISTINCT order_date FROM sales_order", self.engine)

    def getOrderDetailsDataFrame(self):
        orderDetailsQuery = """
        SELECT null AS OrderDetailID, soi.id , so.cust_id, so.order_date, so.sales_rep, soi.prod_id, p.unit_price, soi.quantity
        FROM sales_order_item soi
        JOIN sales_order so ON soi.id = so.id
        JOIN product p ON soi.prod_id = p.id
        """


        return pd.read_sql(orderDetailsQuery, self.engine)
