import lighthouse.config.test as config  # type: ignore
import pyodbc  # type: ignore

cnxn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:host.docker.internal;DATABASE=master;UID=SA;PWD=MyS3cr3tPassw0rd",
    autocommit=True,
)
cursor = cnxn.cursor()
cursor.execute("CREATE DATABASE DartTestDB")
