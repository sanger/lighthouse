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
