import os

import pyodbc

LOCALHOST = os.environ.get("LOCALHOST", "localhost")

cnxn = pyodbc.connect(
    (
        "DRIVER={ODBC Driver 17 for SQL Server};"  # noqa: F541
        f"SERVER=tcp:{LOCALHOST};"
        "DATABASE=master;UID=SA;PWD=MyS3cr3tPassw0rd"
    ),
    autocommit=True,
)
cursor = cnxn.cursor()
cursor.execute("CREATE DATABASE DartTestDB")
