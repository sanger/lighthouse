import pyodbc  # type: ignore

cnxn = pyodbc.connect(
    (
        "DRIVER={ODBC Driver 17 for SQL Server};"  # noqa: F541
        "SERVER=tcp:localhost;"
        "DATABASE=master;UID=SA;PWD=MyS3cr3tPassw0rd"
    ),
    autocommit=True,
)
cursor = cnxn.cursor()
cursor.execute("CREATE DATABASE DartTestDB")
