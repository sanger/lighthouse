import pyodbc  # type: ignore
import logging
from lighthouse.constants import FIELD_DART_DESTINATION_BARCODE

logger = logging.getLogger(__name__)


def create_dart_connection(app):
    return pyodbc.connect(app.config["DART_SQL_SERVER_CONNECTION_STRING"])


COLUMNS_FOR_DART_SAMPLES_TABLE = None


def cache_column_names_for_dart_samples_table(app, cnxn):
    global COLUMNS_FOR_DART_SAMPLES_TABLE
    if COLUMNS_FOR_DART_SAMPLES_TABLE is None:
        cursor = cnxn.cursor()
        COLUMNS_FOR_DART_SAMPLES_TABLE = [column[0] for column in cursor.description]
    return COLUMNS_FOR_DART_SAMPLES_TABLE


def get_columns_for_dart_samples_table():
    return COLUMNS_FOR_DART_SAMPLES_TABLE


def row_to_dict(row):
    if COLUMNS_FOR_DART_SAMPLES_TABLE is None:
        raise "Cannot convert without retrieving the column names first"
    columns = get_columns_for_dart_samples_table()
    obj = {}
    for column in columns:
        obj[column] = getattr(row, column)
    return obj


def get_samples_for_barcode(app, cnxn, barcode):
    cursor = cnxn.cursor()
    cursor.execute(
        f"SELECT * FROM {app.config['DART_RESULT_VIEW']}"
        f" WHERE {FIELD_DART_DESTINATION_BARCODE}='{barcode}';"
    )
    rows = cursor.fetchall()
    return rows


def find_dart_source_samples_rows(app, barcode):
    cnxn = None
    samples = None
    try:
        cnxn = create_dart_connection(app)

        logger.info(f"Querying samples for destination {barcode}")
        samples = get_samples_for_barcode(app, cnxn, barcode)
        logger.info(f"{len(samples)} samples found")
    finally:
        if cnxn is not None:
            cnxn.close()
    return samples


def load_sql_server_script(app, script_path):
    logger.info("Connecting via ODBC")
    conn = create_dart_connection(app)
    logger.info("Connected!\n")

    with open(script_path, "r") as inserts:
        sqlScriptContent = "".join(inserts.readlines())
        for statement in sqlScriptContent.split(";"):
            with conn.cursor() as cur:
                cur.execute(statement)
    logger.info("Loaded script:")
    logger.info(sqlScriptContent)

    conn.close()
    logger.info("Connection closed")
