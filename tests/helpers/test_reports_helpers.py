import os
from datetime import datetime, timedelta
from shutil import copy
from unittest.mock import Mock, patch

import numpy as np
import pandas as pd

from lighthouse.constants.fields import (
    FIELD_COORDINATE,
    FIELD_PLATE_BARCODE,
    FIELD_RESULT,
    FIELD_ROOT_SAMPLE_ID,
    FIELD_SOURCE,
)
from lighthouse.helpers.reports import (
    add_cherrypicked_column,
    delete_reports,
    get_all_positive_samples,
    get_cherrypicked_samples,
    get_distinct_plate_barcodes,
    get_new_report_name_and_path,
    report_query_window_start,
    unpad_coordinate,
)

# ----- get_new_report_name_and_path tests -----


def test_get_new_report_name_and_path(app, freezer):
    report_date = datetime.now().strftime("%y%m%d_%H%M")

    with app.app_context():
        report_name, report_path = get_new_report_name_and_path()

        assert report_name == f"{report_date}_positives_with_locations.xlsx"


# ----- unpad_coordinate tests -----


def test_unpad_coordinate_A01(app, freezer):
    assert unpad_coordinate("A01") == "A1"


def test_unpad_coordinate_A1(app, freezer):
    assert unpad_coordinate("A1") == "A1"


def test_unpad_coordinate_A10(app, freezer):
    assert unpad_coordinate("A10") == "A10"


def test_unpad_coordinate_B01010(app, freezer):
    assert unpad_coordinate("B01010") == "B1010"


# ----- delete_reports tests -----


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
        assert os.path.isfile(f"{app.config['REPORTS_DIR']}/{filename}") is False


# ----- get_cherrypicked_samples tests -----


# Test Scenario
# - Mocking database responses
# - Only the Sentinel query returns matches (No Beckman)
# - No chunking: a single query is made in which all matches are returned
# - No duplication of returned matches
def test_get_cherrypicked_samples_no_beckman(app, freezer):
    expected = [
        pd.DataFrame(
            ["MCM001", "MCM003", "MCM005"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0, 1, 2]
        ),  # Sentinel query response
        pd.DataFrame([]),  # Beckman query response
    ]
    samples = ["MCM001", "MCM002", "MCM003", "MCM004", "MCM005"]
    plate_barcodes = ["123", "456"]

    with app.app_context():
        with patch("sqlalchemy.create_engine", return_value=Mock()):
            with patch(
                "pandas.read_sql",
                side_effect=expected,
            ):
                returned_samples = get_cherrypicked_samples(samples, plate_barcodes)
                assert returned_samples.at[0, FIELD_ROOT_SAMPLE_ID] == "MCM001"
                assert returned_samples.at[1, FIELD_ROOT_SAMPLE_ID] == "MCM003"
                assert returned_samples.at[2, FIELD_ROOT_SAMPLE_ID] == "MCM005"


# Test Scenario
# - Mocking database responses
# - Only the Sentinel queries return matches (No Beckman)
# - Chunking: multiple queries are made, with all matches contained in the sum of these queries
# - No duplication of returned matches
def test_get_cherrypicked_samples_chunking_no_beckman(app, freezer):
    # Note: This represents the results of three different (Sentinel, Beckman) sets of
    # database queries, each Sentinel query getting indexed from 0. Do not change the
    # indices here unless you have modified the behaviour of the query.
    query_results = [
        pd.DataFrame(["MCM001"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0]),  # Sentinel query resp.
        pd.DataFrame([]),  # Beckman query response
        pd.DataFrame(["MCM003"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0]),  # Sentinel query resp.
        pd.DataFrame([]),  # Beckman query response
        pd.DataFrame(["MCM005"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0]),  # Sentinel query resp.
        pd.DataFrame([]),  # Beckman query response
    ]
    expected = pd.DataFrame(["MCM001", "MCM003", "MCM005"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0, 1, 2])

    samples = ["MCM001", "MCM002", "MCM003", "MCM004", "MCM005"]
    plate_barcodes = ["123", "456"]

    with app.app_context():
        with patch("sqlalchemy.create_engine", return_value=Mock()):
            with patch(
                "pandas.read_sql",
                side_effect=query_results,
            ):
                returned_samples = get_cherrypicked_samples(samples, plate_barcodes, 2)
                pd.testing.assert_frame_equal(expected, returned_samples)


# Test Scenario
# - Actual database responses
# - Only the Sentinel queries return matches (No Beckman)
# - Chunking: multiple queries are made, with all matches contained in the sum of these queries
# - Duplication of returned matches across different chunks: duplicates should be filtered out
def test_get_cherrypicked_samples_repeat_tests_no_beckman(app, freezer, mlwh_sentinel_cherrypicked, event_wh_data):
    # the following come from MLWH_SAMPLE_STOCK_RESOURCE in fixture_data
    root_sample_ids = ["root_1", "root_2", "root_1"]
    plate_barcodes = ["pb_1", "pb_2", "pb_3"]

    # root_1 will match 2 samples, but only one of those will match an event (on Sanger Sample Id)
    # therefore we only get 1 of the samples called 'root_1' back (the one on plate 'pb_1')
    # this also checks we don't get a duplicate row for root_1 / pb_1, despite it cropped up in 2
    # different 'chunks'
    expected_rows = [["root_1", "pb_1", "positive", "A1"], ["root_2", "pb_2", "positive", "A1"]]
    expected_columns = [FIELD_ROOT_SAMPLE_ID, FIELD_PLATE_BARCODE, "Result_lower", FIELD_COORDINATE]
    expected = pd.DataFrame(np.array(expected_rows), columns=expected_columns, index=[0, 1])

    with app.app_context():
        chunk_size = 2
        returned_samples = get_cherrypicked_samples(root_sample_ids, plate_barcodes, chunk_size)
        pd.testing.assert_frame_equal(expected, returned_samples)


# Test Scenario
# - Mocking database responses
# - Only the Beckman query returns matches (No Sentinel)
# - No chunking: a single query is made in which all matches are returned
# - No duplication of returned matches
def test_get_cherrypicked_samples_no_sentinel(app, freezer):
    expected = [
        pd.DataFrame([]),  # Sentinel query response
        pd.DataFrame(
            ["MCM001", "MCM003", "MCM005"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0, 1, 2]
        ),  # Beckman query response
    ]
    samples = ["MCM001", "MCM002", "MCM003", "MCM004", "MCM005"]
    plate_barcodes = ["123", "456"]

    with app.app_context():
        with patch("sqlalchemy.create_engine", return_value=Mock()):
            with patch(
                "pandas.read_sql",
                side_effect=expected,
            ):
                returned_samples = get_cherrypicked_samples(samples, plate_barcodes)
                assert returned_samples.at[0, FIELD_ROOT_SAMPLE_ID] == "MCM001"
                assert returned_samples.at[1, FIELD_ROOT_SAMPLE_ID] == "MCM003"
                assert returned_samples.at[2, FIELD_ROOT_SAMPLE_ID] == "MCM005"


# Test Scenario
# - Mocking database responses
# - Only the Beckman queries return matches (No Sentinel)
# - Chunking: multiple queries are made, with all matches contained in the sum of these queries
# - No duplication of returned matches
def test_get_cherrypicked_samples_chunking_no_sentinel(app, freezer):
    # Note: This represents the results of three different (Sentinel, Beckman) sets of
    # database queries, each Sentinel query getting indexed from 0. Do not change the
    # indices here unless you have modified the behaviour of the query.
    query_results = [
        pd.DataFrame([]),  # Sentinel query resp.
        pd.DataFrame(["MCM001"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0]),  # Beckman query resp.
        pd.DataFrame([]),  # Sentinel query resp.
        pd.DataFrame(["MCM003"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0]),  # Beckman query resp.
        pd.DataFrame([]),  # Sentinel query resp.
        pd.DataFrame(["MCM005"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0]),  # Beckman query resp.
    ]
    expected = pd.DataFrame(["MCM001", "MCM003", "MCM005"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0, 1, 2])

    samples = ["MCM001", "MCM002", "MCM003", "MCM004", "MCM005"]
    plate_barcodes = ["123", "456"]

    with app.app_context():
        with patch("sqlalchemy.create_engine", return_value=Mock()):
            with patch(
                "pandas.read_sql",
                side_effect=query_results,
            ):
                returned_samples = get_cherrypicked_samples(samples, plate_barcodes, 2)
                pd.testing.assert_frame_equal(expected, returned_samples)


# Test Scenario
# - Actual database responses
# - Only the Beckman queries return matches (No Sentinel)
# - Chunking: multiple queries are made, with all matches contained in the sum of these queries
# - Duplication of returned matches across different chunks: duplicates should be filtered out
def test_get_cherrypicked_samples_repeat_tests_no_sentinel(app, freezer, mlwh_beckman_cherrypicked, event_wh_data):
    # the following come from MLWH_SAMPLE_LIGHTHOUSE_SAMPLE in fixture_data
    root_sample_ids = ["root_4", "root_5", "root_4"]
    plate_barcodes = ["pb_4", "pb_5", "pb_6"]

    # root_4 will match 2 samples, but only one of those will match an event (on sample uuid)
    # therefore we only get 1 of the samples called 'root_4' back (the one on plate 'pb_4')
    # this also checks we don't get a duplicate row for root_4 / pb_4, despite it cropped up in 2
    # different 'chunks'
    expected_rows = [["root_4", "pb_4", "positive", "A1"], ["root_5", "pb_5", "positive", "A1"]]
    expected_columns = [FIELD_ROOT_SAMPLE_ID, FIELD_PLATE_BARCODE, "Result_lower", FIELD_COORDINATE]
    expected = pd.DataFrame(np.array(expected_rows), columns=expected_columns, index=[0, 1])

    with app.app_context():
        chunk_size = 2
        returned_samples = get_cherrypicked_samples(root_sample_ids, plate_barcodes, chunk_size)
        pd.testing.assert_frame_equal(expected, returned_samples)


# Test Scenario
# - Mocking database responses
# - Both Sentinel and Beckman queries return matches
# - No chunking: a single query is made (per workflow) in which all matches are returned
# - Duplication of returned matches across different workflows: duplicates should be filtered out
def test_get_cherrypicked_samples_sentinel_and_beckman(app, freezer):
    expected = [
        pd.DataFrame(["MCM001", "MCM006"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0, 1]),  # Sentinel query response
        pd.DataFrame(
            ["MCM001", "MCM003", "MCM005"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0, 1, 2]
        ),  # Beckman query response
    ]
    samples = ["MCM001", "MCM002", "MCM003", "MCM004", "MCM005", "MCM006"]
    plate_barcodes = ["123", "456"]

    with app.app_context():
        with patch("sqlalchemy.create_engine", return_value=Mock()):
            with patch(
                "pandas.read_sql",
                side_effect=expected,
            ):
                returned_samples = get_cherrypicked_samples(samples, plate_barcodes)
                assert returned_samples.at[0, FIELD_ROOT_SAMPLE_ID] == "MCM001"
                assert returned_samples.at[1, FIELD_ROOT_SAMPLE_ID] == "MCM006"
                assert returned_samples.at[2, FIELD_ROOT_SAMPLE_ID] == "MCM003"
                assert returned_samples.at[3, FIELD_ROOT_SAMPLE_ID] == "MCM005"


# Test Scenario
# - Mocking database responses
# - Both Sentinel and Beckman queries return matches
# - Chunking: multiple queries are made (per workflow), with all matches contained in the sum
# - Duplication of returned matches across different workflows: duplicates should be filtered out
def test_get_cherrypicked_samples_chunking_sentinel_and_beckman(app, freezer):
    # Note: This represents the results of three different (Sentinel, Beckman) sets of
    # database queries, each query getting indexed from 0. Do not changes the
    # indicies here unless you have modified the behaviour of the query.
    query_results = [
        pd.DataFrame(["MCM001"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0]),  # Sentinel
        pd.DataFrame(["MCM001", "MCM002"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0, 1]),  # Beckman
        pd.DataFrame(["MCM003"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0]),  # Sentinel
        pd.DataFrame(["MCM003", "MCM004"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0, 1]),  # Beckman
        pd.DataFrame(["MCM005"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0]),  # Sentinel
        pd.DataFrame(["MCM005", "MCM006"], columns=[FIELD_ROOT_SAMPLE_ID], index=[0, 1]),  # Beckman
    ]
    expected = pd.DataFrame(
        ["MCM001", "MCM002", "MCM003", "MCM004", "MCM005", "MCM006"],
        columns=[FIELD_ROOT_SAMPLE_ID],
        index=[0, 1, 2, 3, 4, 5],
    )

    samples = ["MCM001", "MCM002", "MCM003", "MCM004", "MCM005"]
    plate_barcodes = ["123", "456"]

    with app.app_context():
        with patch("sqlalchemy.create_engine", return_value=Mock()):
            with patch(
                "pandas.read_sql",
                side_effect=query_results,
            ):
                returned_samples = get_cherrypicked_samples(samples, plate_barcodes, 2)
                pd.testing.assert_frame_equal(expected, returned_samples)


# Test Scenario
# - Actual database responses
# - Both Sentinel and Beckman queries return matches
# - Chunking: multiple queries are made, with all matches contained in the sum of these queries
# - Duplication of returned matches across different chunks: duplicates should be filtered out
def test_get_cherrypicked_samples_repeat_tests_sentinel_and_beckman(
    app, freezer, mlwh_sentinel_and_beckman_cherrypicked, event_wh_data
):
    # the following come from MLWH_SAMPLE_STOCK_RESOURCE and
    # MLWH_SAMPLE_LIGHTHOUSE_SAMPLE in fixture_data
    root_sample_ids = ["root_1", "root_2", "root_3", "root_4", "root_5", "root_1"]
    plate_barcodes = ["pb_1", "pb_2", "pb_3", "pb_4", "pb_5", "pb_6"]

    # root_1 will match 2 samples, but only one of those will match a Sentinel event (on pb_1)
    # root_2 will match a single sample with a matching Sentinel event (on pb_2)
    # root_3 will match 2 samples, but not match either a Sentinel or Beckman event
    # root_4 will match 2 samples, but only one of those will match a Beckman event (on pb_4)
    # root_5 will match a single sample with a matching Beckman event (on pb_5)
    # We also chunk to further test different scenarios
    expected_rows = [
        ["root_1", "pb_1", "positive", "A1"],
        ["root_2", "pb_2", "positive", "A1"],
        ["root_4", "pb_4", "positive", "A1"],
        ["root_5", "pb_5", "positive", "A1"],
    ]
    expected_columns = [FIELD_ROOT_SAMPLE_ID, FIELD_PLATE_BARCODE, "Result_lower", FIELD_COORDINATE]
    expected = pd.DataFrame(np.array(expected_rows), columns=expected_columns, index=[0, 1, 2, 3])

    with app.app_context():
        chunk_size = 2
        returned_samples = get_cherrypicked_samples(root_sample_ids, plate_barcodes, chunk_size)
        pd.testing.assert_frame_equal(expected, returned_samples)


# ----- get_all_positive_samples tests -----


def test_get_all_positive_samples(app, freezer, samples):

    with app.app_context():
        samples = app.data.driver.db.samples
        positive_samples = get_all_positive_samples(samples)

        assert len(positive_samples) == 5
        assert positive_samples.at[0, FIELD_ROOT_SAMPLE_ID] == "sample_001"
        assert positive_samples.at[0, FIELD_RESULT] == "Positive"
        assert positive_samples.at[0, FIELD_SOURCE] == "centre_1"
        assert positive_samples.at[0, FIELD_PLATE_BARCODE] == "plate_123"
        assert positive_samples.at[0, FIELD_COORDINATE] == "A1"
        assert positive_samples.at[0, "plate and well"] == "plate_123:A1"

        assert positive_samples.at[1, FIELD_ROOT_SAMPLE_ID] == "sample_002"
        assert positive_samples.at[2, FIELD_ROOT_SAMPLE_ID] == "sample_003"


# ----- add_cherrypicked_column tests -----


def test_add_cherrypicked_column(app, freezer):
    # existing dataframe before 'add_cherrypicked_column' is run (essentially queried from MongoDB)
    existing_dataframe = pd.DataFrame(
        [
            ["MCM001", "123", "TEST", "Positive", "A1"],
            ["MCM001", "456", "TEST", "Positive", "A1"],  # plate barcode differs from first sample
            ["MCM001", "123", "TEST", "Positive2", "A1"],  # result differs from first sample
            ["MCM001", "123", "TEST", "Positive", "A2"],  # coordinate differs from first sample
            ["MCM002", "123", "TEST", "Positive", "A1"],  # root sample id differs from first sample
        ],
        columns=[
            FIELD_ROOT_SAMPLE_ID,
            FIELD_PLATE_BARCODE,
            "Lab ID",
            FIELD_RESULT,
            FIELD_COORDINATE,
        ],
    )

    # mock response from the 'get_cherrypicked_samples' method
    mock_get_cherrypicked_samples_rows = [
        ["MCM001", "123", "positive", "A1"],  # matches first sample only
        ["MCM002", "123", "positive", "A1"],  # matches final sample only
    ]
    mock_get_cherrypicked_samples_columns = [
        FIELD_ROOT_SAMPLE_ID,
        FIELD_PLATE_BARCODE,
        "Result_lower",
        FIELD_COORDINATE,
    ]
    mock_get_cherrypicked_samples = pd.DataFrame(
        np.array(mock_get_cherrypicked_samples_rows), columns=mock_get_cherrypicked_samples_columns
    )

    # output from 'add_cherrypicked_column' - after merging existing_dataframe with response from
    # 'get_cherrypicked_samples'
    expected_columns = [
        FIELD_ROOT_SAMPLE_ID,
        FIELD_PLATE_BARCODE,
        "Lab ID",
        FIELD_RESULT,
        FIELD_COORDINATE,
        "LIMS submission",
    ]
    # rows with "Yes" are because was returned from get_cherrypicked_samples
    expected_data = [
        [
            "MCM001",
            "123",
            "TEST",
            "Positive",
            "A1",
            "Yes",
        ],
        ["MCM001", "456", "TEST", "Positive", "A1", "No"],
        ["MCM001", "123", "TEST", "Positive2", "A1", "No"],
        ["MCM001", "123", "TEST", "Positive", "A2", "No"],
        [
            "MCM002",
            "123",
            "TEST",
            "Positive",
            "A1",
            "Yes",
        ],
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


def test_add_cherrypicked_column_duplicates(app, freezer):
    # Demonstrates the behaviour where, if 'get_cherrypicked_samples' returns duplicates,
    # 'add_cherrypicked_column' will also return duplicates.
    # De-duping should be handled in 'get_cherrypicked_samples'.

    # existing dataframe before 'add_cherrypicked_column' is run (essentially queried from MongoDB)
    existing_dataframe = pd.DataFrame(
        [["MCM001", "123", "TEST", "Positive", "A1"], ["MCM002", "456", "TEST", "Positive", "A2"]],
        columns=[
            FIELD_ROOT_SAMPLE_ID,
            FIELD_PLATE_BARCODE,
            "Lab ID",
            FIELD_RESULT,
            FIELD_COORDINATE,
        ],
    )

    # mock response from the 'get_cherrypicked_samples' method
    mock_get_cherrypicked_samples_rows = [
        ["MCM002", "456", "positive", "A2"],  # matches second sample
        ["MCM002", "456", "positive", "A2"],  # identical to above
    ]
    mock_get_cherrypicked_samples_columns = [
        FIELD_ROOT_SAMPLE_ID,
        FIELD_PLATE_BARCODE,
        "Result_lower",
        FIELD_COORDINATE,
    ]
    mock_get_cherrypicked_samples = pd.DataFrame(
        np.array(mock_get_cherrypicked_samples_rows), columns=mock_get_cherrypicked_samples_columns
    )

    # output from 'add_cherrypicked_column' - after merging existing_dataframe with response from
    # 'get_cherrypicked_samples'
    expected_columns = [
        FIELD_ROOT_SAMPLE_ID,
        FIELD_PLATE_BARCODE,
        "Lab ID",
        FIELD_RESULT,
        FIELD_COORDINATE,
        "LIMS submission",
    ]
    # Duplicates reflect response from get_cherrypicked_samples
    expected_data = [
        ["MCM001", "123", "TEST", "Positive", "A1", "No"],
        ["MCM002", "456", "TEST", "Positive", "A2", "Yes"],
        [
            "MCM002",
            "456",
            "TEST",
            "Positive",
            "A2",
            "Yes",
        ],
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
        [
            ["MCM001", "123", "TEST", "Positive", "A1"],
            ["MCM002", "123", "TEST", "Positive", "A1"],
        ],
        columns=[
            FIELD_ROOT_SAMPLE_ID,
            FIELD_PLATE_BARCODE,
            "Lab ID",
            FIELD_RESULT,
            FIELD_COORDINATE,
        ],
    )

    # Not sure if this is an accurate mock - haven't tried it with a real db connection
    mock_get_cherrypicked_samples = pd.DataFrame(
        [], columns=[FIELD_ROOT_SAMPLE_ID, FIELD_PLATE_BARCODE, "Result_lower", FIELD_COORDINATE]
    )

    expected_columns = [
        FIELD_ROOT_SAMPLE_ID,
        FIELD_PLATE_BARCODE,
        "Lab ID",
        FIELD_RESULT,
        FIELD_COORDINATE,
        "LIMS submission",
    ]
    expected_data = [
        ["MCM001", "123", "TEST", "Positive", "A1", "No"],
        ["MCM002", "123", "TEST", "Positive", "A1", "No"],
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


# ----- get_distinct_plate_barcodes tests -----


def test_get_distinct_plate_barcodes(app, freezer, samples):

    with app.app_context():
        samples = app.data.driver.db.samples

        assert get_distinct_plate_barcodes(samples)[0] == "plate_123"


def test_report_query_window_start(app):
    with app.app_context():
        window_size = app.config["REPORT_WINDOW_SIZE"]
        start = datetime.now() + timedelta(days=-window_size)

        assert report_query_window_start().year == start.year
        assert report_query_window_start().month == start.month
        assert report_query_window_start().day == start.day
        assert report_query_window_start().hour == 0
        assert report_query_window_start().minute == 0
        assert report_query_window_start().second == 0
