import logging

import pyodbc
from flask import current_app as app

logger = logging.getLogger(__name__)


def create_dart_connection():
    """Create a connection to the DART database using the pyodbc library."""
    logger.info("Connecting to DART using pyodbc")
    return pyodbc.connect(app.config["DART_SQL_SERVER_CONNECTION_STRING"])


def load_sql_server_script(script_path: str) -> None:
    logger.info("Executing DART SQL script")

    connection = create_dart_connection()

    with open(script_path, "r") as file:
        dart_seed_sql = "".join(file.readlines())

        logger.debug(dart_seed_sql)

        for statement in dart_seed_sql.split(";"):
            with connection.cursor() as cursor:
                cursor.execute(statement)
