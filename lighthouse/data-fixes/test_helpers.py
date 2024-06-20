# helpers for testing e.g. just print all the data out, populate the local DB etc.
import pandas as pd
import sqlalchemy
import pymongo
import mysql.connector

from constants import (
    MYSQL_DB_CONN_STRING,
    MYSQL_PWD,
    MYSQL_USER,
    MYSQL_HOST,
    MLWH_DB,
    MONGO_DB,
    MONGO_DB_CLIENT,
    MONGO_TABLE,
    SQL_GET_ALL_DATA,
    malformed_csv,
    control_csv,
    skippable_csv
)

def print_data():
    try:
        mlwh_db = MLWH_DB
        print('connecting to DB')
        sql_engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{MYSQL_DB_CONN_STRING}/{mlwh_db}", pool_recycle=3600
        )
        db_connection = sql_engine.connect()
        print('getting data')
        data = pd.read_sql(SQL_GET_ALL_DATA, db_connection)
        print('got data')
        print(data)
    except Exception as e:
        print("Error while connecting to MLWH.")
        print(e)
        return None
    finally:
        if db_connection is not None:
            print("Closing MLWH connection.")
            db_connection.close()

def populate_local_db(database):
    malformed = pd.read_csv(malformed_csv)
    skippable = pd.read_csv(skippable_csv)
    control = pd.read_csv(control_csv)

    data = pd.concat([malformed, skippable, control])
    data_no_current_rna = data.drop(columns=['current_rna_id'])

    if database == "mysql":
        populate_mysql(data_no_current_rna)
    elif database == "mongo":
        populate_mongo(data_no_current_rna)
    else:
        print("Not a valid DB type")
        return None

def populate_mongo(data):
    try:
        client = pymongo.MongoClient(MONGO_DB_CLIENT)
        db = client[MONGO_DB]
        table = db[MONGO_TABLE]
        data_dict = data.to_dict()
        print(data_dict)
        table.insert_many([data_dict])
    except Exception as e:
        print("Error while connecting to Mongo DB.")
        print(e)
        return None

def populate_mysql(data):
    try:
        mlwh_db = MLWH_DB
        print('connecting to DB')
        sql_engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{MYSQL_DB_CONN_STRING}/{mlwh_db}", pool_recycle=3600
        )
        db_connection = sql_engine.connect()
        data.to_sql('lighthouse_sample', db_connection, if_exists='replace', index=False, chunksize=1)
    except Exception as e:
        print("Error while connecting to MySQL")
        print(e)
        return None
    finally:
        if db_connection is not None:
            print("Closing mlwh connection")
            db_connection.close()
        return None

def find_duplicate_root_sample_ids(root_sample_ids):
    print("Attempting to connect to DB.")
    try:
        db_connection = mysql.connector.connect(host = MYSQL_HOST,
                                                database = MLWH_DB,
                                                user = MYSQL_USER,
                                                password = MYSQL_PWD,
                                                port = '3436')
        full_data = pd.DataFrame()
        print("Loading the data...")
        cursor = db_connection.cursor()
        for index, row in root_sample_ids.iterrows():
            if index % 1000 == 0:
                print("Reached index "+ str(index))
            root_sample_id = row["root_sample_id"]
            plate_barcode = row["plate_barcode"]
            coordinate = row["coordinate"]
            select_query = (
                f"SELECT root_sample_id, plate_barcode, coordinate"
                f" FROM lighthouse_sample"
                f" WHERE root_sample_id = '{root_sample_id}'"
                f" AND plate_barcode = '{plate_barcode}'"
                f" AND coordinate = '{coordinate}'"
            )
            cursor.execute(select_query)
            db_data = cursor.fetchall()
            data_row = pd.DataFrame(db_data)
            full_data = pd.concat([full_data, data_row])
        cursor.close()
        print("Data loaded in successfully.")
    except Exception as e:
        print("Error while connecting to MySQL")
        print(e)
        return None
    finally:
        if db_connection is not None:
            print("Closing DB connection.")
            db_connection.close()
        return full_data
