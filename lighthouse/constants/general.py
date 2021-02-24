# arguments to extract from a request
ARG_BARCODE = "barcode"
ARG_USER_ID = "user_id"
ARG_ROBOT_SERIAL = "robot"
ARG_FAILURE_TYPE = "failure_type"

# Columns that should appear in the fit to pick samples report and the order in which they will appear
REPORT_COLUMNS = [
    "Date Tested",
    "Root Sample ID",
    "Result",
    "source",
    "plate_barcode",
    "coordinate",
    "plate and well",
    "location_barcode",
    "LIMS submission",
]

# Facets for the aggregation query to mongo
FACET_FIT_TO_PICK_SAMPLES = "fit_to_pick_samples"
FACET_COUNT_FIT_TO_PICK_SAMPLES = "count_fit_to_pick_samples"
FACET_COUNT_FILTERED_POSITIVE = "count_filtered_positive"
FACET_COUNT_MUST_SEQUENCE = "count_must_sequence"
FACET_COUNT_PREFERENTIALLY_SEQUENCE = "count_preferentially_sequence"
FACET_DISTINCT_PLATE_BARCODE = "distinct_plate_barcode"
