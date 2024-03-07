# take the CSV data and insert corrected IDs into the various DBs
import pymongo
import mysql.connector
import pandas as pd
from argparse import ArgumentParser

from constants import (
    FIXED_DATA_COL_NAME,
    MLWH_COLUMN_NAME,
    MONGO_COLUMN_NAME,
    MYSQL_HOST,
    MYSQL_PORT,
    MONGO_DB,
    MONGO_DB_HOST,
    MONGO_DB_AUTH_SOURCE,
    MONGO_DB_USER,
    MONGO_DB_PASSWORD,
    MONGO_TABLE,
    MYSQL_USER,
    MYSQL_PWD,
    MLWH_DB,
    MLWH_TABLE,
    fixed_data_file
)

def write_data_to_db(data: pd.DataFrame, database: str):
    if database.lower() == "mongo":
        write_to_mongo(data)
    elif database.lower() == "mysql":
        write_to_mysql(data)
    else:
        print("Not a valid DB type")
        return None

def write_to_mongo(data):
    print("Attempting to connect to Mongo DB...")
    try:
        client = pymongo.MongoClient(MONGO_DB_HOST,
                                     username=MONGO_DB_USER,
                                     password=MONGO_DB_PASSWORD,
                                     authSource=MONGO_DB_AUTH_SOURCE)
        db = client[MONGO_DB]
        table = db[MONGO_TABLE]
        print("Loading in the data...")
        for index, row in data.iterrows():
            new_value = row[FIXED_DATA_COL_NAME]
            root_sample_id = row["root_sample_id"]
            lab_id = row["lab_id"]
            result = row["result"]
            rna_id = row["rna_id"]
            update_query = { "Lab ID": lab_id, "Result": result, "Root Sample ID": root_sample_id, "RNA ID": rna_id }
            new_value_query = { "$set": { MONGO_COLUMN_NAME: new_value } }
            table.update_many(update_query, new_value_query)
        print("Data loaded in successfully.")
    except Exception as e:
        print("Error while connecting to Mongo DB.")
        print(e)
        return None

def write_to_mysql(data):
    print("Attempting to connect to MLWH...")
    try:
        db_connection = mysql.connector.connect(host=MYSQL_HOST,
                                                database=MLWH_DB,
                                                user=MYSQL_USER,
                                                password=MYSQL_PWD,
                                                port=MYSQL_PORT)
        print("Loading in the data...")
        cursor = db_connection.cursor()
        for index, row in data.iterrows():
            new_value = row[FIXED_DATA_COL_NAME]
            root_sample_id = row["root_sample_id"]
            lab_id = row["lab_id"]
            result = row["result"]
            rna_id = row["rna_id"]
            update_query = (
                f"UPDATE {MLWH_TABLE}"
                f" SET {MLWH_COLUMN_NAME} = '{new_value}'"
                f" WHERE root_sample_id = '{root_sample_id} AND lab_id = '{lab_id}' AND result = '{result}' AND rna_id = '{rna_id}'"
            )
            try:
                cursor.execute(update_query)
                db_connection.commit()
            except Exception:
                pass
        cursor.close()
        print("Data loaded in successfully.")
    except Exception as e:
        print("Error while connecting to MLWH.")
        print(e)
        return None
    finally:
        if db_connection is not None:
            print("Closing MLWH connection.")
            db_connection.close()
        return

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--db")
    args = parser.parse_args()
    db = vars(args)["db"]
    data = pd.read_csv(fixed_data_file)
    write_data_to_db(data, db)
