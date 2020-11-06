import os
import pyodbc  # type: ignore
import logging
from lighthouse.constants import FIELD_DART_DESTINATION_BARCODE

logger = logging.getLogger(__name__)


def create_dart_connection(app):
    return pyodbc.connect(app.config["DART_SQL_SERVER_CONNECTION_STRING"])


def find_dart_source_samples_rows(app, barcode):
    cnxn = create_dart_connection(app)
    cursor = cnxn.cursor()
    logger.info(f"Querying samples for destination {barcode}")
    cursor.execute(
        f"SELECT * from {app.config['DART_RESULT_VIEW']} where {FIELD_DART_DESTINATION_BARCODE}='{barcode}';"
    )
    rows = cursor.fetchall()
    logger.info(f"{len(rows)} samples found")
    return rows


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
