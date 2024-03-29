from lighthouse.constants.fields import (
    FIELD_COG_BARCODE,
    FIELD_COORDINATE,
    FIELD_DART_CONTROL,
    FIELD_DART_DESTINATION_BARCODE,
    FIELD_DART_DESTINATION_COORDINATE,
    FIELD_DART_LAB_ID,
    FIELD_DART_LH_SAMPLE_UUID,
    FIELD_DART_RNA_ID,
    FIELD_DART_ROOT_SAMPLE_ID,
    FIELD_DART_SOURCE_BARCODE,
    FIELD_DART_SOURCE_COORDINATE,
    FIELD_LAB_ID,
    FIELD_LH_SAMPLE_UUID,
    FIELD_PLATE_BARCODE,
    FIELD_RESULT,
    FIELD_RNA_ID,
    FIELD_ROOT_SAMPLE_ID,
    FIELD_SOURCE,
)

DART_MONGO_MERGED_SAMPLES = [
    {  # Control sample
        "sample": None,
        "row": {
            FIELD_DART_DESTINATION_COORDINATE: "B01",
            FIELD_DART_DESTINATION_BARCODE: "d123",
            FIELD_DART_CONTROL: "positive",
            FIELD_DART_SOURCE_BARCODE: "123",
            FIELD_DART_SOURCE_COORDINATE: "A01",
            FIELD_DART_ROOT_SAMPLE_ID: "",
            FIELD_DART_RNA_ID: "",
            FIELD_DART_LAB_ID: "",
            FIELD_DART_LH_SAMPLE_UUID: "plate_3",
        },
    },
    {  # Non-control sample
        "sample": {
            FIELD_COORDINATE: "A02",
            FIELD_SOURCE: "test2",
            FIELD_RESULT: "Positive",
            FIELD_PLATE_BARCODE: "1234",
            FIELD_COG_BARCODE: "abcd",
            FIELD_ROOT_SAMPLE_ID: "MCM002",
            FIELD_RNA_ID: "rna_2",
            FIELD_LAB_ID: "AP",
            FIELD_LH_SAMPLE_UUID: "plate_3",
        },
        "row": {
            FIELD_DART_DESTINATION_COORDINATE: "B02",
            FIELD_DART_DESTINATION_BARCODE: "d123",
            FIELD_DART_CONTROL: "",
            FIELD_DART_SOURCE_BARCODE: "1234",
            FIELD_DART_SOURCE_COORDINATE: "A02",
            FIELD_DART_ROOT_SAMPLE_ID: "MCM002",
            FIELD_DART_RNA_ID: "rna_2",
            FIELD_DART_LAB_ID: "AB",
            FIELD_DART_LH_SAMPLE_UUID: "plate_3",
        },
    },
]
