# get the data from MLWH - use the SQL_MLWH_GET_MALFORMED_DATA constant in constants.py to give the SQL call for the data
import sqlalchemy
import pandas as pd

from constants import (
    MYSQL_DB_CONN_STRING,
    MLWH_DB,
    SQL_MLWH_GET_MALFORMED_DATA
)

def get_data() -> pd.DataFrame:
    print("Attempting to connect to MLWH.")
    try:
        sql_engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{MYSQL_DB_CONN_STRING}/{MLWH_DB}", pool_recycle=3600
        )
        db_connection = sql_engine.connect()
        print("Connected to MLWH... getting data.")
        data = pd.read_sql(SQL_MLWH_GET_MALFORMED_DATA, db_connection)
        print("Got the data.")
    except Exception as e:
        print("Error while connecting to MLWH.")
        print(e)
        return None
    finally:
        if db_connection is not None:
            print("Closing MLWH connection.")
            db_connection.close()
            return data
