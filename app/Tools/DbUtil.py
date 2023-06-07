def constructConnectionString(dbRef):
    dbName = dbRef

    username = 'floep'
    password = 'WaaromWilDePausNietGecremeerdWorden?HijLeeftNog'

    server = 'outdoorfusionserver.database.windows.net'
    driver = '{ODBC Driver 17 for SQL Server}'
    trustedConnection = 'no'

    dbc = f"DRIVER={driver};SERVER={server};DATABASE={dbName};UID={username};PWD={password};trusted_connection={trustedConnection}"

    return dbc
