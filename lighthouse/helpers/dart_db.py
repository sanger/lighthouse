import logging

import pyodbc  # type: ignore
from flask import current_app as app
from lighthouse.constants import (
    FIELD_DART_CONTROL,
    FIELD_DART_DESTINATION_BARCODE,
    FIELD_DART_LAB_ID,
    FIELD_DART_RNA_ID,
    FIELD_DART_ROOT_SAMPLE_ID,
    FIELD_DART_RUN_ID,
)

logger = logging.getLogger(__name__)


def create_dart_connection():
    return pyodbc.connect(app.config["DART_SQL_SERVER_CONNECTION_STRING"])


def get_samples_for_barcode(cnxn, barcode):
    cursor = cnxn.cursor()
    cursor.execute(
        f"SELECT * FROM {app.config['DART_RESULT_VIEW']}"
        f" WHERE [{FIELD_DART_DESTINATION_BARCODE}]='{barcode}'"
        f" AND (([{FIELD_DART_ROOT_SAMPLE_ID}] IS NOT NULL"
        f" AND [{FIELD_DART_ROOT_SAMPLE_ID}]<>''"
        f" AND [{FIELD_DART_RNA_ID}] IS NOT NULL"
        f" AND [{FIELD_DART_RNA_ID}]<>''"
        f" AND [{FIELD_DART_LAB_ID}] IS NOT NULL"
        f" AND [{FIELD_DART_LAB_ID}]<>'')"
        f" OR ([{FIELD_DART_CONTROL}] IS NOT NULL AND [{FIELD_DART_CONTROL}]<>''))"
        f" AND [{FIELD_DART_RUN_ID}]=("
        f"  SELECT MAX([{FIELD_DART_RUN_ID}])"
        f"  FROM {app.config['DART_RESULT_VIEW']}"
        f"  WHERE [{FIELD_DART_DESTINATION_BARCODE}]='{barcode}');"
    )
    rows = cursor.fetchall()
    return rows


def find_dart_source_samples_rows(barcode):
    cnxn = None
    samples = None
    try:
        cnxn = create_dart_connection()

        logger.info(f"Querying samples for destination {barcode}")
        samples = get_samples_for_barcode(cnxn, barcode)
        logger.info(f"{len(samples)} samples found")
    finally:
        if cnxn is not None:
            cnxn.close()
    return samples


def load_sql_server_script(app, script_path):
    logger.info("Connecting via ODBC")
    conn = create_dart_connection()
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
