import os

import pyodbc

LOCALHOST = os.environ.get("LOCALHOST", "127.0.0.1")

cnxn = pyodbc.connect(
    (
        "DRIVER={ODBC Driver 18 for SQL Server};"  # noqa: F541
        f"SERVER=tcp:{LOCALHOST};"
        "DATABASE=master;UID=SA;PWD=MyS3cr3tPassw0rd;TrustServerCertificate=yes"
    ),
    autocommit=True,
)
cursor = cnxn.cursor()
cursor.execute("CREATE DATABASE DartTestDB;")
