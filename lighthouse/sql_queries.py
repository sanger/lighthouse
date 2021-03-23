from lighthouse.constants.fields import (
    FIELD_ROOT_SAMPLE_ID,
    FIELD_PLATE_BARCODE,
    FIELD_COORDINATE,
)

SQL_MLWH_GET_CP_SAMPLES = (
    f"SELECT root_sample_id AS `{FIELD_ROOT_SAMPLE_ID}`, `{FIELD_PLATE_BARCODE}`,"
    f" phenotype AS `Result_lower`, `{FIELD_COORDINATE}`"
    f" FROM cherrypicked_samples"
    f" WHERE root_sample_id IN %(root_sample_ids)s"
    f" AND `{FIELD_PLATE_BARCODE}` IN %(plate_barcodes)s"
)
