import lighthouse.config.test as config  # type: ignore
import pyodbc  # type: ignore

cnxn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:localhost;DATABASE=master;UID=SA;PWD=MyV3rY@7742w0rd",
    autocommit=True,
)
cursor = cnxn.cursor()
cursor.execute("CREATE DATABASE DartTestDB")
