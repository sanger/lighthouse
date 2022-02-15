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


class DartServiceMixin:
    def get_samples_for_destination_barcode(self, connection: Any, destination_barcode: str) -> List[Any]:
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


    def find_dart_source_samples_rows(self, barcode: str) -> List[Any]:
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
        #connection = create_dart_connection()

        #samples = self.get_samples_for_destination_barcode(connection, barcode)
        #self.convert_to_dict(samples)
        self.convert_to_dict([])

        return samples


    def convert_to_dict(self, rows):
        import collection   
        samples = []
        for row in rows:
            row_dict = collections.OrderedDict()
            row_dict['automation_system_run_id'] = row[FIELD_DART_RUN_ID]
            row_dict['created_at'] = ""
            row_dict['date_picked'] = ""
            row_dict['destination_coordinate'] = row[FIELD_DART_DESTINATION_COORDINATE]
            row_dict['lab_id'] = row[FIELD_DART_LAB_ID]
            row_dict['lh_sample_uuid'] = row[FIELD_DART__LH_SAMPLE_UUID]
            row_dict['picked'] = True
            row_dict['rna_id'] = row[FIELD_DART_RNA_ID]
            row_dict['source_barcode'] = row[FIELD_DART_DESTINATION_BARCODE]
            row_dict['source_coordinate'] = row[FIELD_DART_SOURCE_COORDINATE]
            row_dict['type'] = "sample"
            samples.append(row_dict)

        #return samples
        return SOURCE_PLATE_WELLS



        SOURCE_PLATE_WELLS = [
    {
        FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_RUN_ID: 1,
        FIELD_CHERRYTRACK_DESTINATION_BARCODE: "DN00000001",
        FIELD_CHERRYTRACK_DESTINATION_COORDINATE: "H6",
        FIELD_CHERRYTRACK_LAB_ID: "lab_1",
        FIELD_CHERRYTRACK_LH_SAMPLE_UUID: "c15a694f-a4db-44f4-9a98-6c1804197f01",
        FIELD_CHERRYTRACK_PICKED: True,
        FIELD_CHERRYTRACK_RNA_ID: "RNA-S-00001-00000004",
        FIELD_BARCODE: "plate_123",
        FIELD_CHERRYTRACK_SOURCE_BARCODE: "DS000010003",
        FIELD_CHERRYTRACK_SOURCE_COORDINATE: "A4",
        FIELD_CHERRYTRACK_TYPE: "sample",
    },
    {
        FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_RUN_ID: 1,
        FIELD_CHERRYTRACK_DESTINATION_BARCODE: "DN00000001",
        FIELD_CHERRYTRACK_DESTINATION_COORDINATE: "H3",
        FIELD_CHERRYTRACK_LAB_ID: "lab_2",
        FIELD_CHERRYTRACK_LH_SAMPLE_UUID: "c4cc673e-3da0-47da-b754-ae01b7c6095e",
        FIELD_CHERRYTRACK_PICKED: True,
        FIELD_CHERRYTRACK_RNA_ID: "RNA-S-00001-00000001",
        FIELD_CHERRYTRACK_SOURCE_BARCODE: "plate_456",
        FIELD_CHERRYTRACK_SOURCE_COORDINATE: "A6",
        FIELD_CHERRYTRACK_TYPE: "sample",
    },
    {
        FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_RUN_ID: 1,
        FIELD_CHERRYTRACK_DESTINATION_BARCODE: "DN00000001",
        FIELD_CHERRYTRACK_DESTINATION_COORDINATE: "H12",
        FIELD_CHERRYTRACK_LAB_ID: "lab_2",
        FIELD_CHERRYTRACK_LH_SAMPLE_UUID: "da95a299-1ad4-4620-aaf1-4ba7ab21522f",
        FIELD_CHERRYTRACK_PICKED: True,
        FIELD_CHERRYTRACK_RNA_ID: "RNA-S-00001-00000009",
        FIELD_CHERRYTRACK_SOURCE_BARCODE: "plate_789",
        FIELD_CHERRYTRACK_SOURCE_COORDINATE: "B4",
        FIELD_CHERRYTRACK_TYPE: "sample",
    },
    {
        FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_RUN_ID: 1,
        FIELD_CHERRYTRACK_DESTINATION_BARCODE: "DN00000001",
        FIELD_CHERRYTRACK_DESTINATION_COORDINATE: "H8",
        FIELD_CHERRYTRACK_LAB_ID: "lab_3",
        FIELD_CHERRYTRACK_LH_SAMPLE_UUID: "5e9d1b1a-2c32-4921-87f5-770032bec951",
        FIELD_CHERRYTRACK_PICKED: True,
        FIELD_CHERRYTRACK_RNA_ID: "RNA-S-00001-00000006",
        FIELD_CHERRYTRACK_SOURCE_BARCODE: "plate_abc",
        FIELD_CHERRYTRACK_SOURCE_COORDINATE: "C7",
        FIELD_CHERRYTRACK_TYPE: "sample",
    },
]

