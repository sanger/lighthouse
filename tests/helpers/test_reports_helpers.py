from datetime import datetime
from shutil import copy
import os

import pandas as pd
import numpy as np
from unittest.mock import patch, Mock

from lighthouse.helpers.reports import (
    get_new_report_name_and_path,
    unpad_coordinate,
    delete_reports,
    get_cherrypicked_samples,
    get_all_positive_samples,
    map_labware_to_location,
    add_cherrypicked_column,
    get_distinct_plate_barcodes,
    join_samples_declarations,
)
from lighthouse.exceptions import ReportCreationError
from lighthouse.constants import (
    FIELD_COORDINATE,
    FIELD_ROOT_SAMPLE_ID,
    FIELD_RESULT,
    FIELD_PLATE_BARCODE,
    FIELD_SOURCE,
    FIELD_CH1_CQ,
    CT_VALUE_LIMIT
)

def test_get_new_report_name_and_path(app, freezer):
    report_date = datetime.now().strftime("%y%m%d_%H%M")

    with app.app_context():
        report_name, report_path = get_new_report_name_and_path()

        assert report_name == f"{report_date}_positives_with_locations.xlsx"


def test_unpad_coordinate_A01(app, freezer):
    assert unpad_coordinate("A01") == "A1"


def test_unpad_coordinate_A1(app, freezer):
    assert unpad_coordinate("A1") == "A1"


def test_unpad_coordinate_A10(app, freezer):
    assert unpad_coordinate("A10") == "A10"


def test_unpad_coordinate_B01010(app, freezer):
    assert unpad_coordinate("B01010") == "B1010"


def test_delete_reports(app, freezer):

    copies_of_reports_folder = "tests/data/reports_copies"

    filenames = [
        "200716_1345_positives_with_locations.xlsx",
        "200716_1618_positives_with_locations.xlsx",
        "200716_1640_positives_with_locations.xlsx",
        "200716_1641_positives_with_locations.xlsx",
        "200716_1642_positives_with_locations.xlsx",
    ]

    for filename in filenames:
        copy(f"{copies_of_reports_folder}/{filename}", f"{app.config['REPORTS_DIR']}/{filename}")

    with app.app_context():
        delete_reports(filenames)

    for filename in filenames:
        assert os.path.isfile(f"{app.config['REPORTS_DIR']}/{filename}") == False


def test_get_cherrypicked_samples(app, freezer):

    expected = pd.DataFrame(
        ["MCM001", "MCM003", "MCM005"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0, 1, 2]
    )
    samples = ["MCM001", "MCM002", "MCM003", "MCM004", "MCM005"]
    plate_barcodes = ["123", "456"]

    with app.app_context():
        with patch("sqlalchemy.create_engine", return_value=Mock()):
            with patch(
                "pandas.read_sql", return_value=expected,
            ):
                returned_samples = get_cherrypicked_samples(samples, plate_barcodes)
                assert returned_samples.at[0, FIELD_ROOT_SAMPLE_ID] == "MCM001"
                assert returned_samples.at[1, FIELD_ROOT_SAMPLE_ID] == "MCM003"
                assert returned_samples.at[2, FIELD_ROOT_SAMPLE_ID] == "MCM005"


def test_get_all_positive_samples(app, freezer, samples):

    with app.app_context():
        samples = app.data.driver.db.samples
        positive_samples = get_all_positive_samples(samples)

        assert len(positive_samples) == 3
        assert positive_samples.at[0,FIELD_ROOT_SAMPLE_ID] == 'MCM001'
        assert positive_samples.at[0,FIELD_RESULT] == 'Positive'
        assert positive_samples.at[0,FIELD_SOURCE] == 'test1'
        assert positive_samples.at[0,FIELD_PLATE_BARCODE] == '123'
        assert positive_samples.at[0,FIELD_COORDINATE] == 'A1'
        assert positive_samples.at[0,'plate and well'] == '123:A1'

        assert positive_samples.at[1,FIELD_ROOT_SAMPLE_ID] == 'MCM005'
        assert positive_samples.at[2,FIELD_ROOT_SAMPLE_ID] == 'MCM007'


def test_query_by_ct_limit(app, freezer, samples_ct_values):
    # Just testing how mongo queries work with 'less than' comparisons and nulls
    with app.app_context():
        samples = app.data.driver.db.samples
        ct_less_than_limit = samples.count_documents( { FIELD_CH1_CQ: {"$lte": CT_VALUE_LIMIT} } )

        assert ct_less_than_limit == 1 # 'MCM003'


def test_map_labware_to_location_labwhere_error(app, freezer, labwhere_samples_error):
    # mocks response from get_locations_from_labwhere() with labwhere_samples_error

    raised_exception = False

    try:
        with app.app_context():
            map_labware_to_location(["test"])
    except ReportCreationError:
        raised_exception = True

    assert raised_exception


def test_map_labware_to_location_dataframe_content(app, freezer, labwhere_samples_multiple):
    # mocks response from get_locations_from_labwhere() with labwhere_samples_multiple
    with app.app_context():
        result = map_labware_to_location(
            ["123", "456", "789"]
        )  # '789' returns no location, in the mock

    expected_columns = [FIELD_PLATE_BARCODE, "location_barcode"]
    expected_data = [["123", "4567"], ["456", "1234"], ["789", ""]]
    assert result.columns.to_list() == expected_columns
    assert np.array_equal(result.to_numpy(), expected_data)


def test_add_cherrypicked_column(app, freezer):
    # mocks response from get_cherrypicked_samples()
    existing_dataframe = pd.DataFrame(
        [["MCM001", "123", "TEST"], ["MCM002", "123", "TEST"], ["MCM003", "123", "TEST"]],
        columns=[FIELD_ROOT_SAMPLE_ID, FIELD_PLATE_BARCODE, "Lab ID"],
    )

    mock_get_cherrypicked_samples = pd.DataFrame(["MCM001", "MCM003"], columns=[FIELD_ROOT_SAMPLE_ID])

    expected_columns = [FIELD_ROOT_SAMPLE_ID, FIELD_PLATE_BARCODE, "Lab ID", "LIMS submission"]
    expected_data = [
        ["MCM001", "123", "TEST", "Yes"],
        ["MCM002", "123", "TEST", "No"],
        ["MCM003", "123", "TEST", "Yes"],
    ]

    with app.app_context():
        with patch("sqlalchemy.create_engine", return_value=Mock()):
            with patch(
                "lighthouse.helpers.reports.get_cherrypicked_samples",
                return_value=mock_get_cherrypicked_samples,
            ):

                new_dataframe = add_cherrypicked_column(existing_dataframe)

    assert new_dataframe.columns.to_list() == expected_columns
    assert np.array_equal(new_dataframe.to_numpy(), expected_data)


def test_add_cherrypicked_column_no_rows(app, freezer):
    # mocks response from get_cherrypicked_samples()
    existing_dataframe = pd.DataFrame(
        [["MCM001", "123", "TEST"], ["MCM002", "123", "TEST"],],
        columns=[FIELD_ROOT_SAMPLE_ID, FIELD_PLATE_BARCODE, "Lab ID"],
    )

    # Not sure if this is an accurate mock - haven't tried it with a real db connection
    mock_get_cherrypicked_samples = pd.DataFrame([], columns=[FIELD_ROOT_SAMPLE_ID])

    expected_columns = [FIELD_ROOT_SAMPLE_ID, FIELD_PLATE_BARCODE, "Lab ID", "LIMS submission"]
    expected_data = [["MCM001", "123", "TEST", "No"], ["MCM002", "123", "TEST", "No"]]

    with app.app_context():
        with patch("sqlalchemy.create_engine", return_value=Mock()):
            with patch(
                "lighthouse.helpers.reports.get_cherrypicked_samples",
                return_value=mock_get_cherrypicked_samples,
            ):

                new_dataframe = add_cherrypicked_column(existing_dataframe)

    assert new_dataframe.columns.to_list() == expected_columns
    assert np.array_equal(new_dataframe.to_numpy(), expected_data)


def test_get_distinct_plate_barcodes(app, freezer, samples):

    with app.app_context():
        samples = app.data.driver.db.samples

        assert get_distinct_plate_barcodes(samples)[0] == "123"


def test_join_samples_declarations(app, freezer, samples_declarations, samples_no_declaration):

    with app.app_context():
        samples = app.data.driver.db.samples
        positive_samples = get_all_positive_samples(samples)
        joined = join_samples_declarations(positive_samples)

        assert joined.at[1, FIELD_ROOT_SAMPLE_ID] == "MCM010"
        assert joined.at[1, "Value In Sequencing"] == "Unknown"


def test_join_samples_declarations_empty_collection(app, freezer, samples_no_declaration):
    # samples_declaration collection is empty because we are not passing in the fixture

    with app.app_context():
        samples = app.data.driver.db.samples
        positive_samples = get_all_positive_samples(samples)
        joined = join_samples_declarations(positive_samples)

        assert np.array_equal(positive_samples.to_numpy(), joined.to_numpy())
