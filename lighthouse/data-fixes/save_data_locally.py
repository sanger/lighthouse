# get the data, fix it, write these to a CSV to be used with the 'write_data' script (which inserts the fixed data into the DBs)
import pandas as pd
import argparse
import sqlalchemy

from data_helpers import remove_everything_after_first_underscore

from constants import (
    FIXED_DATA_COL_NAME,
    ORIGINAL_DATA_COL_NAME,
    MYSQL_DB_CONN_STRING,
    MLWH_DB,
    SQL_MLWH_GET_MALFORMED_DATA
)

def save_data(input_filename, output_filename):
    if input_filename:
        data = pd.read_csv(input_filename)
    else:
        data = get_data()

    print("Editing the data...")
    data = data.rename(columns={FIXED_DATA_COL_NAME: ORIGINAL_DATA_COL_NAME})
    data[FIXED_DATA_COL_NAME] = data[ORIGINAL_DATA_COL_NAME].apply(remove_everything_after_first_underscore)
    print("Adding the data to a CSV file.")
    data.to_csv(output_filename, index=False)

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=False)
    parser.add_argument("--output_file", required=True)
    args = parser.parse_args()
    input_filename = vars(args)["input_file"]
    output_filename = vars(args)["output_file"]
    save_data(input_filename=input_filename, output_filename=output_filename)
