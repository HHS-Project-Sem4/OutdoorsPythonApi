def constructConnectionString(dbRef):
    dbName = dbRef

    server = 'outdoorfusionserver.database.windows.net'
    username = 'floep'
    password = 'WaaromWilDePausNietGecremeerdWorden?HijLeeftNog'
    driver = '{ODBC Driver 17 for SQL Server}'
    trustedConnection = 'no'

    dbc = f"DRIVER={driver};SERVER={server};DATABASE={dbName};UID={username};PWD={password};trusted_connection={trustedConnection}"

    return dbc
