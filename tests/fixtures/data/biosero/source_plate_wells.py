from lighthouse.constants.fields import (
    FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_RUN_ID,
    FIELD_CHERRYTRACK_DESTINATION_BARCODE,
    FIELD_CHERRYTRACK_DESTINATION_COORDINATE,
    FIELD_CHERRYTRACK_LAB_ID,
    FIELD_CHERRYTRACK_LH_SAMPLE_UUID,
    FIELD_CHERRYTRACK_PICKED,
    FIELD_CHERRYTRACK_RNA_ID,
    FIELD_BARCODE,
    FIELD_CHERRYTRACK_SOURCE_BARCODE,
    FIELD_CHERRYTRACK_SOURCE_COORDINATE,
    FIELD_CHERRYTRACK_TYPE,
)

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