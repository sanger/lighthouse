# take the CSV data and insert corrected IDs into the various DBs
import pymongo
import mysql.connector
import pandas as pd
import argparse

from constants import (LOCALHOST, MONGO_DB, MONGO_DB_CLIENT, MONGO_TABLE, MYSQL_USER, MYSQL_PWD, MLWH_DB, fixed_samples_file)

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
        client = pymongo.MongoClient(MONGO_DB_CLIENT)
        db = client[MONGO_DB]
        table = db[MONGO_TABLE]
        print("Loading in the data...")
        for index, row in data.iterrows():
            root_sample_id = row["root_sample_id"]
            original_root_sample_id = row["original_root_sample_id"]

            update_query = { "Root Sample ID": original_root_sample_id }
            new_value = { "$set": { "Root Sample ID": root_sample_id } }

            table.update_one(update_query, new_value)
        print("Data loaded in successfully.")
    except Exception as e:
        print("Error while connecting to MongoDB")
        print(e)
        return None

def write_to_mysql(data):
    print("Attempting to connect to MLWH...")
    try:
        db_connection = mysql.connector.connect(host = LOCALHOST,
                                                database = MLWH_DB,
                                                user = MYSQL_USER,
                                                password = MYSQL_PWD)
        print("Loading in the data...")
        cursor = db_connection.cursor()
        for index, row in data.iterrows():
            root_sample_id = row["root_sample_id"]
            original_root_sample_id = row["original_root_sample_id"]
            update_query = (
                f"UPDATE lighthouse_sample"
                f" SET root_sample_id = '{root_sample_id}'"
                f" WHERE root_sample_id = '{original_root_sample_id}'"
            )
            cursor.execute(update_query)
            rows_updated = cursor.rowcount
            db_connection.commit()
        cursor.close()
        print("Data loaded in successfully.")
    except Exception as e:
        print("Error while connecting to MySQL")
        print(e)
        return None
    finally:
        if db_connection is not None:
            print("Closing MLWH connection.")
            db_connection.close()
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db")
    args = parser.parse_args()
    db = vars(args)["db"]
    data = pd.read_csv(fixed_samples_file)
    write_data_to_db(data, db)
