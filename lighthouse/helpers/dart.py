import logging
from typing import Any, List

from flask import current_app as app

from lighthouse.constants.fields import (
    FIELD_DART_CONTROL,
    FIELD_DART_DESTINATION_BARCODE,
    FIELD_DART_LAB_ID,
    FIELD_DART_RNA_ID,
    FIELD_DART_ROOT_SAMPLE_ID,
    FIELD_DART_RUN_ID,
)
from lighthouse.db.dart import create_dart_connection

logger = logging.getLogger(__name__)


def get_samples_for_destination_barcode(connection: Any, destination_barcode: str) -> List[Any]:
    """Get the samples for a destination barcode from DART.

    Arguments:
        connection (Any): the connection to the DART database.
        destination_barcode (str): destination barcode to get samples for.

    Returns:
        List[Any]: from pyodbc documentation: "Returns a list of all the remaining rows in the query."
    """
    logger.info(
        f"SELECT-ing from DART '{app.config['DART_RESULT_VIEW']}' view for "
        f"{FIELD_DART_DESTINATION_BARCODE}: {destination_barcode}"
    )
    cursor = connection.cursor()

    cursor.execute(
        f"SELECT * FROM {app.config['DART_RESULT_VIEW']}"
        f" WHERE [{FIELD_DART_DESTINATION_BARCODE}]='{destination_barcode}'"
        f" AND (([{FIELD_DART_ROOT_SAMPLE_ID}] IS NOT NULL"
        f" AND [{FIELD_DART_ROOT_SAMPLE_ID}]<>''"
        f" AND [{FIELD_DART_RNA_ID}] IS NOT NULL"
        f" AND [{FIELD_DART_RNA_ID}] <> ''"
        f" AND [{FIELD_DART_LAB_ID}] IS NOT NULL"
        f" AND [{FIELD_DART_LAB_ID}] <> '')"
        f" OR ([{FIELD_DART_CONTROL}] IS NOT NULL AND [{FIELD_DART_CONTROL}] <> ''))"
        f" AND [{FIELD_DART_RUN_ID}]=("
        f"  SELECT MAX([{FIELD_DART_RUN_ID}])"
        f"  FROM {app.config['DART_RESULT_VIEW']}"
        f"  WHERE [{FIELD_DART_DESTINATION_BARCODE}]='{destination_barcode}');"
    )

    rows: List[Any] = cursor.fetchall()

    logger.info(f"{len(rows)} samples found in DART view")

    return rows


def find_dart_source_samples_rows(barcode: str) -> List[Any]:
    """Find the samples in DART for a given barcode.

    Arguments:
        barcode (str): barcode to query.

    Returns:
        List[Any]: rows of samples.
    """
    logger.info(f"Querying samples for destination plate with barcode: {barcode}")

    # "Connections are automatically closed when they are deleted (typically when they go out of scope) so you should
    #   not normally need to call this (.close())
    #   https://github.com/mkleehammer/pyodbc/wiki/Connection#close
    connection = create_dart_connection()

    samples = get_samples_for_destination_barcode(connection, barcode)

    return samples
