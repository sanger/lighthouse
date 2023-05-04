from http import HTTPStatus
from unittest.mock import patch

import pandas as pd
import pytest

from lighthouse.constants.fields import FIELD_COORDINATE, FIELD_PLATE_BARCODE, FIELD_ROOT_SAMPLE_ID
from lighthouse.constants.general import REPORT_COLUMNS

ENDPOINT_PREFIXES = ["", "/v1"]

GET_REPORTS_ENDPOINT = "/reports"
POST_NEW_REPORT_ENDPOINT = "/reports/new"
DELETE_REPORTS_ENDPOINT = "/delete_reports"

GET_REPORTS_ENDPOINTS = [prefix + GET_REPORTS_ENDPOINT for prefix in ENDPOINT_PREFIXES]
POST_NEW_REPORT_ENDPOINTS = [prefix + POST_NEW_REPORT_ENDPOINT for prefix in ENDPOINT_PREFIXES]
DELETE_REPORTS_ENDPOINTS = [prefix + DELETE_REPORTS_ENDPOINT for prefix in ENDPOINT_PREFIXES]


@pytest.mark.parametrize("endpoint", GET_REPORTS_ENDPOINTS)
def test_get_reports_endpoint(client, endpoint):
    with patch("lighthouse.routes.common.reports.get_reports_details", return_value=[]):
        response = client.get(endpoint)

        assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize("endpoint", GET_REPORTS_ENDPOINTS)
def test_get_reports_list(client, endpoint):
    with patch("lighthouse.routes.common.reports.get_reports_details", return_value=[]):
        response = client.get(endpoint)

        assert response.json == {"reports": []}


@pytest.mark.parametrize("endpoint", POST_NEW_REPORT_ENDPOINTS)
def test_create_report(client, app, tmp_path, samples, labwhere_samples_simple, endpoint):
    with app.app_context():
        with patch(
            "lighthouse.jobs.reports.get_new_report_name_and_path", return_value=["test.xlsx", f"{tmp_path}/test.xlsx"]
        ):
            with patch("lighthouse.routes.common.reports.get_reports_details", return_value="Some details of a report"):
                cherrypicked_df = pd.DataFrame(
                    [["MCM001", "pb_1", "Positive", "A1"]],
                    columns=[FIELD_ROOT_SAMPLE_ID, FIELD_PLATE_BARCODE, "Result_lower", FIELD_COORDINATE],
                )
                with patch("lighthouse.helpers.reports.get_cherrypicked_samples", return_value=cherrypicked_df):
                    response = client.post(endpoint)

                    assert response.json == {"reports": "Some details of a report"}
                    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize("endpoint", POST_NEW_REPORT_ENDPOINTS)
def test_report_columns(client, app, tmp_path, samples, labwhere_samples_simple, endpoint):
    with app.app_context():
        test_xlsx = "test.xlsx"
        test_path = f"{tmp_path}/{test_xlsx}"
        with patch("lighthouse.jobs.reports.get_new_report_name_and_path", return_value=[test_xlsx, test_path]):
            with patch(
                "lighthouse.routes.common.reports.get_reports_details",
                return_value=(report_details := "Some details of a report"),
            ):
                response = client.post(endpoint)
                assert response.json == {"reports": report_details}

                data_frame = pd.read_excel(test_path)
                assert sorted(data_frame.columns) == sorted(REPORT_COLUMNS)


@pytest.mark.parametrize("endpoint", DELETE_REPORTS_ENDPOINTS)
def test_delete_reports_endpoint(client, endpoint):
    with patch("lighthouse.routes.common.reports.delete_reports", return_value=None):
        json_body = {
            "data": {
                "filenames": [
                    "200716_1345_positives_with_locations.xlsx",
                    "200716_1618_positives_with_locations.xlsx",
                    "200716_1640_positives_with_locations.xlsx",
                    "200716_1641_fit_to_pick_with_locations.xlsx",
                    "200716_1642_fit_to_pick_with_locations.xlsx",
                ]
            }
        }

        response = client.post(endpoint, json=json_body)

        assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize("endpoint", DELETE_REPORTS_ENDPOINTS)
def test_delete_reports_endpoint_fails(client, endpoint):
    with patch("lighthouse.routes.common.reports.delete_reports", return_value=None):
        response = client.post(endpoint, json="{}")

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
