from lighthouse.constants.fields import (
    FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_RUN_ID,
    FIELD_CHERRYTRACK_DESTINATION_COORDINATE,
    FIELD_CHERRYTRACK_LAB_ID,
    FIELD_CHERRYTRACK_LH_SAMPLE_UUID,
    FIELD_CHERRYTRACK_RNA_ID,
    FIELD_CHERRYTRACK_SOURCE_BARCODE,
    FIELD_CHERRYTRACK_SOURCE_COORDINATE,
    FIELD_CHERRYTRACK_TYPE,
)

DESTINATION_PLATE_WELLS = [
    {
        FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_RUN_ID: 1,
        FIELD_CHERRYTRACK_DESTINATION_COORDINATE: "A1",
        FIELD_CHERRYTRACK_LAB_ID: "MK",
        FIELD_CHERRYTRACK_LH_SAMPLE_UUID: "268b8b62-132c-4acb-ac4e-bb186965ae90",
        FIELD_CHERRYTRACK_RNA_ID: "RNA-S-00001-00000001",
        FIELD_CHERRYTRACK_SOURCE_BARCODE: "DS000010001",
        FIELD_CHERRYTRACK_SOURCE_COORDINATE: "H2",
        FIELD_CHERRYTRACK_TYPE: "sample",
    },
    {
        FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_RUN_ID: 1,
        FIELD_CHERRYTRACK_DESTINATION_COORDINATE: "A2",
        FIELD_CHERRYTRACK_LAB_ID: "MK",
        FIELD_CHERRYTRACK_LH_SAMPLE_UUID: "a93ba9f9-757e-4eb6-9d40-489110758502",
        FIELD_CHERRYTRACK_RNA_ID: "RNA-S-00001-00000002",
        FIELD_CHERRYTRACK_SOURCE_BARCODE: "DS000010001",
        FIELD_CHERRYTRACK_SOURCE_COORDINATE: "D12",
        FIELD_CHERRYTRACK_TYPE: "sample",
    },
    {
        FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_RUN_ID: 1,
        FIELD_CHERRYTRACK_DESTINATION_COORDINATE: "A3",
        FIELD_CHERRYTRACK_LAB_ID: "MK",
        FIELD_CHERRYTRACK_LH_SAMPLE_UUID: "07624bfa-e0d6-48cc-b612-38ce25c8274a",
        FIELD_CHERRYTRACK_RNA_ID: "RNA-S-00001-00000003",
        FIELD_CHERRYTRACK_SOURCE_BARCODE: "DS000010001",
        FIELD_CHERRYTRACK_SOURCE_COORDINATE: "G6",
        FIELD_CHERRYTRACK_TYPE: "sample",
    },
    {
        FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_RUN_ID: 1,
        FIELD_CHERRYTRACK_DESTINATION_COORDINATE: "A4",
        FIELD_CHERRYTRACK_LAB_ID: "MK",
        FIELD_CHERRYTRACK_LH_SAMPLE_UUID: "5d8541de-3a8f-4536-80d3-e451cec2d0c0",
        FIELD_CHERRYTRACK_RNA_ID: "RNA-S-00001-00000004",
        FIELD_CHERRYTRACK_SOURCE_BARCODE: "DS000010001",
        FIELD_CHERRYTRACK_SOURCE_COORDINATE: "E6",
        FIELD_CHERRYTRACK_TYPE: "sample",
    },
]


def build_cherrytrack_destination_plate_response(destination_barcode, source_barcode, run_id):
    return {
        "data": {
            "barcode": destination_barcode,
            "wells": [
                {
                    "type": "sample",
                    "source_barcode": source_barcode,
                    "source_coordinate": "A1",
                    "destination_coordinate": "H08",
                    "rna_id": f"{source_barcode}_A01",
                    "root_sample_id": "aRootSampleId1",
                    "result": "Positive",
                    "lab_id": "centre_1",
                    "lh_sample_uuid": "aLighthouseUUID1",
                    "run_id": run_id,
                },
                {
                    "type": "sample",
                    "source_barcode": source_barcode,
                    "source_coordinate": "A3",
                    "destination_coordinate": "H12",
                    "rna_id": f"{source_barcode}_A03",
                    "root_sample_id": "aRootSampleId2",
                    "result": "Positive",
                    "lab_id": "centre_2",
                    "lh_sample_uuid": "aLighthouseUUID3",
                    "run_id": run_id - 1,
                },
                {
                    "type": "control",
                    "control_barcode": "DN1234",
                    "control_coordinate": "A1",
                    "destination_coordinate": "E10",
                    "control": "positive",
                    "run_id": run_id - 2,
                },
                {
                    "type": "control",
                    "control_barcode": "DN1234",
                    "control_coordinate": "A1",
                    "destination_coordinate": "E11",
                    "control": "negative",
                    "run_id": run_id - 2,
                },
            ],
        }
    }
