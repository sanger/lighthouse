from datetime import datetime
from shutil import copy
import os

from lighthouse.helpers.reports import (
    get_new_report_name_and_path,
    unpad_coordinate,
    delete_reports,
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
