# Sentinel workflow event to help determine sample cherrypicked status
EVENT_CHERRYPICK_LAYOUT_SET = "cherrypick_layout_set"

###
# Events detailed: https://ssg-confluence.internal.sanger.ac.uk/display/PSDPUB/Cherrypicking+Events
# Source plate has had all pickable wells cherrypicked into destination plates, and the plate is
# put into the output stacks.
# Cherrypicking source and destination plate events
###
PLATE_EVENT_SOURCE_COMPLETED = "lh_beckman_cp_source_completed"
# Source plate barcode cannot be read (damaged or missing), and the plate is put into the output
# stacks.
PLATE_EVENT_SOURCE_NOT_RECOGNISED = "lh_beckman_cp_source_plate_unrecognised"
# Source plate has no related plate map data, cannot be cherrypicked (yet), and the plate is
# returned to the input
# stacks.
PLATE_EVENT_SOURCE_NO_MAP_DATA = "lh_beckman_cp_source_no_plate_map_data"
# Source plate only contains negatives, nothing to cherrypick, and the plate is put into the output
# stacks.
PLATE_EVENT_SOURCE_ALL_NEGATIVES = "lh_beckman_cp_source_all_negatives"
# Destination plate has been created successfully
PLATE_EVENT_DESTINATION_CREATED = "lh_beckman_cp_destination_created"
# Destination plate has failed to be created successfully
PLATE_EVENT_DESTINATION_FAILED = "lh_beckman_cp_destination_failed"
