from datetime import datetime
from shutil import copy
import os

import pandas as pd
from unittest.mock import patch, Mock

from lighthouse.helpers.reports import (
    get_new_report_name_and_path,
    unpad_coordinate,
    delete_reports,
    get_cherrypicked_samples,
    get_all_positive_samples
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

  expected = pd.DataFrame(['MCM001', 'MCM003', 'MCM005'], columns=['description'], index=[0, 1, 2])
  samples = "MCM001,MCM002,MCM003,MCM004,MCM005"

  with app.app_context():
    with patch(
      "sqlalchemy.create_engine", return_value=Mock()
    ):
      with patch(
          "pandas.read_sql", return_value=expected,
        ):
        returned_samples = get_cherrypicked_samples(samples)
        assert returned_samples.at[0, 'description'] == "MCM001"
        assert returned_samples.at[1, 'description'] == "MCM003"
        assert returned_samples.at[2, 'description'] == "MCM005"

def test_get_all_positive_samples(app, freezer, samples):

    # sample = samples[0]
    # sample = { 'Root Sample ID'	'Result'	'Date Tested'	'source'	'plate_barcode'	'coordinate'	'plate and well'}
    # expected = pd.DataFrame(['MCM001', 'MCM003', 'MCM005'], columns=['description'], index=[0, 1, 2])

#     Root Sample ID	Result	Date Tested	source	plate_barcode	coordinate	plate and well	location_barcode
# LEI00009968	Positive	2020-05-10 18:53:47 UTC	Alderley	AP-rna-00111417	H8	AP-rna-00111417:H8	lw-uk-bio--19-14576
    assert get_all_positive_samples() == True
