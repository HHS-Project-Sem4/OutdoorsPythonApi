import pandas as pd


# methods for modifying current dataframes

# Creates a new dataframe containing a Date as id and three columns for Month, Quarter and Year
def createDayDateDataframe(sourceFrame, sourceColumn, dateFormat):
    dateColumns = ['DAY_date', 'DAY_MONTH_nr', 'DAY_QUARTER_nr', 'DAY_YEAR_nr']
    DAY_date = pd.DataFrame(columns=dateColumns)

    sourceFrame[sourceColumn] = pd.to_datetime(sourceFrame[sourceColumn], format=dateFormat)

    for index, row in sourceFrame.iterrows():
        return_date = row[sourceColumn]

        date_values = [return_date.month, (return_date.month - 1) // 3 + 1, return_date.year]

        date_frame = pd.DataFrame([[return_date, date_values[0], date_values[1], date_values[2]]],
                                  columns=['DAY_date', 'DAY_MONTH_nr', 'DAY_QUARTER_nr', 'DAY_YEAR_nr'])
        DAY_date = pd.concat([DAY_date, date_frame], ignore_index=True)

    return DAY_date


def addUniqueIntIdColumn(dataFrame, columnName, newColumn):
    originalFrame = dataFrame.copy()

    uniqueValues = originalFrame[columnName].unique()
    originalFrame[newColumn] = pd.Series(dtype='Int32')

    newId = 0

    for value in uniqueValues:
        condition = originalFrame[columnName] == value
        originalFrame.loc[condition, newColumn] = newId

        newId += 1

    return originalFrame


# Adds an unorganised range of Ids of type int to a column
def addIntID(sourceFrame, idColumnName):
    originalFrame = sourceFrame.copy()

    id_list = range(len(originalFrame))
    originalFrame[idColumnName] = id_list

    return originalFrame


# Splits a pandas DataFrame based on unique values in columns
def splitDataFrame(sourceFrame, idColumnName, childColumns):
    originalFrame = sourceFrame.copy()

    selectedSplitColumns = [idColumnName]
    selectedSplitColumns.extend(childColumns)

    splitFrame = originalFrame[selectedSplitColumns]
    splitFrame = splitFrame.drop_duplicates(subset=[idColumnName])

    removeColumns = childColumns.copy()

    originalColumns = sourceFrame.columns.tolist()
    newOriginalColumns = [column for column in originalColumns if column not in removeColumns]
    originalFrame = originalFrame[newOriginalColumns]

    return [originalFrame, splitFrame]


# methods concerning merging

def mergeStarDiagrams(baseStarDiagram, addedStarDiagram, factFrameName, factFramePrimaryKey, factFrameNonLinkedIds,
                      idRegex):
    resultFrame = baseStarDiagram.copy()

    baseFactFrame = next((df for df in resultFrame if df.name == factFrameName), None)
    addedFactFrame = next((df for df in addedStarDiagram if df.name == factFrameName), None)

    for baseTable, addTable in zip(baseStarDiagram, addedStarDiagram):
        tableName = addTable.name

        # fixes ids for the connected dataframes
        if addTable.name != factFrameName:
            for column in addTable.columns:
                if idRegex in column:
                    createUniqueLinkedIds(baseFactFrame, addedFactFrame, addTable, column)

        # fixes ids for the factframe primary key for the table can just be from baseframe.max() till (len(toadd) + baseframe.max)
        # columns that are not linked will get a unique id
        else:
            for column in addTable.columns:
                if column == factFramePrimaryKey:
                    createUniqueNonLinkedIds(baseFactFrame, addTable, column)
                if column in factFrameNonLinkedIds:
                    addTable = createUniqueIds(baseTable, column, addTable)

        # merges dataframe
        baseTable = pd.concat([baseTable, addTable])
        baseTable.name = tableName

        # adds merged dataframe to the resulting star diagram
        resultFrame = [baseTable if df.name == tableName else df for df in resultFrame]

    return resultFrame

def createUniqueIds(baseFactFrame, column, dataFrame):
    originalFrame = dataFrame.copy()

    uniqueValues = originalFrame[column].unique()
    newId = getMaxIdValue(baseFactFrame, column)

    for value in uniqueValues:
        condition = originalFrame[column] == value
        originalFrame.loc[condition, column] = newId

        newId += 1

    return originalFrame


# Creates a set of new ids for an ID column that is not linked to something, range of ids starts at the max of the baseframe similair id column
def createUniqueNonLinkedIds(baseFactFrame, frameToFix, column):
    newIDValue = getMaxIdValue(baseFactFrame, column)

    id_list = range(newIDValue, (newIDValue + len(frameToFix)))
    frameToFix[column] = id_list


# Creates new IDS and links to the factframe, doesnt change the id for -1 values because it assumes -1 is null from previous data cleaning
def createUniqueLinkedIds(baseFactFrame, addedFactFrame, frameToFix, column):
    newIDValue = getMaxIdValue(baseFactFrame, column)

    for index, value in frameToFix[column].items():

        if value != -1:
            condition1 = addedFactFrame[column] == value
            addedFactFrame.loc[condition1, column] = newIDValue

            condition1 = frameToFix[column] == value
            frameToFix.loc[condition1, column] = newIDValue

            newIDValue += 1


def getMaxIdValue(dataFrame, column):
    newIDValue = 0

    if dataFrame is not None:
        if not (pd.isna(dataFrame[column].max())):
            newIDValue = dataFrame[column].max()
            newIDValue += 5000

    return newIDValue


def checkColumnForDuplicates(df, colomnRegex):
    for table in df:
        for column in table:
            if colomnRegex in column:
                duplicate_count = table[column].duplicated().sum()
                print(f'COLUMN: {column} HAS {duplicate_count} OF DUPLICATED VALUES')


def createEmptyStarFrame():
    column_data = [
        {'name': 'Product',
         'columns': ['PRODUCT_id', 'PRODUCT_name', 'PRODUCT_category', 'PRODUCT_sub_category', 'PRODUCT_colour',
                     'PRODUCT_prod_cost', 'PRODUCT_storage_quantity'], 'dtype': {'PRODUCT_id': 'Int32'}},
        {'name': 'Customer',
         'columns': ['CUSTOMER_id', 'CUSTOMER_address', 'CUSTOMER_city', 'CUSTOMER_state', 'CUSTOMER_region',
                     'CUSTOMER_country', 'CUSTOMER_company_name'], 'dtype': {'CUSTOMER_id': 'Int32'}},
        {'name': 'Employee',
         'columns': ['EMPLOYEE_id', 'EMPLOYEE_first_name', 'EMPLOYEE_last_name', 'EMPLOYEE_city', 'EMPLOYEE_state',
                     'EMPLOYEE_region', 'EMPLOYEE_country'], 'dtype': {'EMPLOYEE_id': 'Int32'}},
        {'name': 'Order_Date', 'columns': ['DAY_date', 'DAY_MONTH_nr', 'DAY_QUARTER_nr', 'DAY_YEAR_nr'],
         'dtype': {'DAY_date': 'datetime64[ns]', 'DAY_MONTH_nr': 'Int8', 'DAY_QUARTER_nr': 'Int8',
                   'DAY_YEAR_nr': 'Int16'}},
        {'name': 'Order_Details',
         'columns': ['ORDER_DETAIL_id', 'ORDER_HEADER_id', 'ORDER_DETAIL_order_quantity', 'ORDER_DETAIL_unit_price',
                     'DAY_date', 'EMPLOYEE_id', 'CUSTOMER_id', 'PRODUCT_id'],
         'dtype': {'ORDER_DETAIL_id': 'Int32', 'ORDER_HEADER_id': 'Int32', 'DAY_date': 'datetime64[ns]',
                   'EMPLOYEE_id': 'Int32', 'CUSTOMER_id': 'Int32', 'PRODUCT_id': 'Int32'}}
    ]

    data = []
    for item in column_data:
        df = pd.DataFrame(columns=item['columns']).astype(item['dtype'])
        df.name = item['name']
        data.append(df)

    return data
