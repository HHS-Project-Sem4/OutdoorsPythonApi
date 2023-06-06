import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


def findAll(connectionString,table):
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connectionString})

    engine = create_engine(connection_url)

    return pd.read_sql(f'SELECT * FROM {table}', engine)
