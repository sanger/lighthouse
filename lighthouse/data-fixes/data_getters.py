# get the root_sample_ids from MLWH - any root_sample_ids containing an underscore
import sqlalchemy
import pandas as pd

from constants import MYSQL_DB_CONN_STRING, MLWH_DB, SQL_MLWH_GET_MALFORMED_ROOT_IDS

def get_data() -> pd.DataFrame:
    print("Attempting to connect to DB.")
    try:
        sql_engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{MYSQL_DB_CONN_STRING}/{MLWH_DB}", pool_recycle=3600
        )
        db_connection = sql_engine.connect()
        print("Connected to the DB... getting data.")
        data = pd.read_sql(SQL_MLWH_GET_MALFORMED_ROOT_IDS, db_connection)
        print("Got the data.")
    except Exception as e:
        print("Error while connecting to MySQL")
        print(e)
        return None
    finally:
        if db_connection is not None:
            print("Closing DB connection.")
            db_connection.close()
            return data
