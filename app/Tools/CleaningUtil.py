import pandas as pd


def CleanCustomer(dataFrame):
    table = dataFrame.copy()

    expectedTypes = {'CUSTOMER_id': 'Int32',
                     'CUSTOMER_address': 'string',
                     'CUSTOMER_city': 'string',
                     'CUSTOMER_state': 'string',
                     'CUSTOMER_region': 'string',
                     'CUSTOMER_country': 'string',
                     'CUSTOMER_company_name': 'string'}

    table = table.astype(expectedTypes)

    table.name = 'Customer'
    return table


def cleanEmployee(dataFrame):
    table = dataFrame.copy()

    expectedTypes = {'EMPLOYEE_id': 'Int32',
                     'EMPLOYEE_first_name': 'string',
                     'EMPLOYEE_last_name': 'string',
                     'EMPLOYEE_city': 'string',
                     'EMPLOYEE_state': 'string',
                     'EMPLOYEE_region': 'string',
                     'EMPLOYEE_country': 'string'}

    table = table.astype(expectedTypes)

    table.name = 'Employee'
    return table


def cleanProduct(dataFrame):
    table = dataFrame.copy()

    table = setAllToString(table)

    expectedTypes = {'PRODUCT_id': 'Int32',
                     'PRODUCT_name': 'string',
                     'PRODUCT_category': 'string',
                     'PRODUCT_sub_category': 'string',
                     'PRODUCT_colour': 'string',
                     'PRODUCT_prod_cost': 'float',
                     'PRODUCT_storage_quantity': 'Int32'}

    table = table.astype(expectedTypes)

    table['PRODUCT_prod_cost'] = table['PRODUCT_prod_cost'].fillna(0)
    table['PRODUCT_storage_quantity'] = table['PRODUCT_storage_quantity'].fillna(0)

    table.name = 'Product'
    return table


def cleanOrderDetails(dataFrame):
    table = dataFrame.copy()

    table = setAllToString(table)
    print(table.columns)

    expectedTypes = {'ORDER_DETAIL_id': 'Int32',
                     'ORDER_HEADER_id': 'Int32',
                     'ORDER_DETAIL_order_quantity': 'Int32',
                     'ORDER_DETAIL_unit_price': 'float',
                     'EMPLOYEE_id': 'Int32',
                     'CUSTOMER_id': 'Int32',
                     'PRODUCT_id': 'Int32'}

    table = table.astype(expectedTypes)

    for column in table.columns:
        if '_id' in column:
            table[column] = table[column].fillna(0)
        elif 'date' in column:
            table[column] = table[column].fillna('1900-01-01')
        else:
            table[column] = table[column].fillna(0)


    table.name = 'Order_Details'

    return table


def setAllToString(dataFrame):
    table = dataFrame.copy()

    for col in table.columns:
        changeType = {col: 'string'}
        table = table.astype(changeType)

    return table

def cleanDayDate(dataFrame):
    table = dataFrame.copy()

    table.name = 'Order_Date'
    return table