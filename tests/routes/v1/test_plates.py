from http import HTTPStatus
from typing import List, Optional
from unittest.mock import patch

import pytest
import responses
from responses.matchers import query_param_matcher

from lighthouse.constants.config import SS_PLATE_TYPE_DEFAULT
from lighthouse.constants.general import ARG_EXCLUDE, ARG_TYPE, ARG_TYPE_DESTINATION, ARG_TYPE_SOURCE

ENDPOINT_PREFIXES = ["", "/v1"]
NEW_PLATE_ENDPOINT = "/plates/new"
GET_PLATES_ENDPOINT = "/plates"
CHERRYTRACK_PLATES_ENDPOINT = ["/plates/cherrytrack"]

NEW_PLATE_ENDPOINTS = [prefix + NEW_PLATE_ENDPOINT for prefix in ENDPOINT_PREFIXES]
GET_PLATES_ENDPOINTS = [prefix + GET_PLATES_ENDPOINT for prefix in ENDPOINT_PREFIXES]

FIT_TO_PICK_PLATE_TYPES: List[Optional[str]] = [None, SS_PLATE_TYPE_DEFAULT, "fit_to_pick_new_samples_only"]
ALL_SAMPLES_PLATE_TYPES: List[Optional[str]] = ["all_samples", "all_new_samples_only"]

VALID_PLATE_BARCODE = "plate_123"
INVALID_PLATE_BARCODE = "qwerty"
EMPTY_PLATE_BARCODE = "plate_empty"

LOOKUP_LABWARE_ERROR_JSON = {"errors": ["Labware lookup failed."]}
LOOKUP_SAMPLES_ERROR_JSON = {"errors": ["Samples lookup failed."]}
CREATE_PLATE_ERROR_JSON = {"errors": ["The barcode 'plate_123' is not a recognised format."]}

QUERY_PARAM_BARCODE = "barcode"
QUERY_PARAM_BARCODES = "barcodes"


def create_plate_body(barcode, plate_type=None):
    body = {QUERY_PARAM_BARCODE: barcode}

    if plate_type is not None:
        body["type"] = plate_type

    return body


def mock_labware_lookup(app, mocked_responses, labware_found_count=0):
    ss_url = f"{app.config['SS_URL']}/api/v2/labware"

    for _ in range(labware_found_count):
        mocked_responses.add(responses.GET, ss_url, json={"data": [{"some labware": "data"}]}, status=HTTPStatus.OK)

    if labware_found_count == 0:
        mocked_responses.add(responses.GET, ss_url, json={"data": []}, status=HTTPStatus.OK)


def mock_labware_lookup_failure(app, mocked_responses):
    ss_url = f"{app.config['SS_URL']}/api/v2/labware"
    mocked_responses.add(responses.GET, ss_url, json=LOOKUP_LABWARE_ERROR_JSON, status=HTTPStatus.UNPROCESSABLE_ENTITY)


def mock_samples_lookup(app, mocked_responses, found_samples_count=0, mock_missing_samples=True):
    ss_url = f"{app.config['SS_URL']}/api/v2/samples"

    for _ in range(found_samples_count):
        mocked_responses.add(responses.GET, ss_url, json={"data": [{"some sample": "data"}]}, status=HTTPStatus.OK)

    if mock_missing_samples:
        mocked_responses.add(responses.GET, ss_url, json={"data": []}, status=HTTPStatus.OK)


def mock_samples_lookup_failure(app, mocked_responses):
    ss_url = f"{app.config['SS_URL']}/api/v2/samples"
    mocked_responses.add(responses.GET, ss_url, json=LOOKUP_SAMPLES_ERROR_JSON, status=HTTPStatus.UNPROCESSABLE_ENTITY)


def mock_plate_create(app, mocked_responses, success_body=None):
    ss_url = f"{app.config['SS_URL']}/api/v2/heron/plates"

    if success_body:
        body = success_body
        status = HTTPStatus.CREATED
    else:
        body = CREATE_PLATE_ERROR_JSON
        status = HTTPStatus.UNPROCESSABLE_ENTITY

    mocked_responses.add(responses.POST, ss_url, json=body, status=status)


@pytest.fixture
def logger():
    with patch("lighthouse.routes.common.plates.LOGGER") as mock:
        yield mock


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
def test_post_plates_endpoint_successful_with_no_plate_type_and_all_cog_barcodes_already_in_samples(
    app, client, samples, source_plates, priority_samples, mocked_responses, mlwh_lh_samples, endpoint
):
    body = create_plate_body(VALID_PLATE_BARCODE)
    mock_plate_create(app, mocked_responses, body)

    response = client.post(endpoint, json=body)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {
        "data": {"plate_barcode": "plate_123", "centre": "centre_1", "count_fit_to_pick_samples": 5}
    }


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
def test_post_plates_endpoint_successful_with_default_fit_to_pick_plate_type_and_all_cog_barcodes_already_in_samples(
    app, client, samples, source_plates, priority_samples, mocked_responses, mlwh_lh_samples, endpoint
):
    body = create_plate_body(VALID_PLATE_BARCODE, SS_PLATE_TYPE_DEFAULT)
    mock_plate_create(app, mocked_responses, body)

    response = client.post(endpoint, json=body)
    assert response.status_code == HTTPStatus.CREATED

    # There should be 5 fit to pick samples even though more exist for the plate.
    assert response.json == {
        "data": {"plate_barcode": VALID_PLATE_BARCODE, "centre": "centre_1", "count_fit_to_pick_samples": 5}
    }


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
def test_post_plates_endpoint_logs_warning_and_successful_with_fit_to_pick_new_samples_only_plate_type(
    app, client, samples, source_plates, priority_samples, mocked_responses, mlwh_lh_samples, logger, endpoint
):
    body = create_plate_body(VALID_PLATE_BARCODE, "fit_to_pick_new_samples_only")
    mock_plate_create(app, mocked_responses, body)

    response = client.post(endpoint, json=body)

    logger.warning.assert_called_once()
    assert "does not support this configuration" in logger.warning.call_args.args[0]
    assert VALID_PLATE_BARCODE in logger.warning.call_args.args[0]

    # The plate will be created as usual which is detailed in the warning
    assert response.status_code == HTTPStatus.CREATED

    # There should be 5 fit to pick samples even though more exist for the plate.
    assert response.json == {
        "data": {"plate_barcode": VALID_PLATE_BARCODE, "centre": "centre_1", "count_fit_to_pick_samples": 5}
    }


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
def test_post_plates_endpoint_successful_with_all_samples_plate_type_and_all_cog_barcodes_already_in_samples(
    app, client, samples, source_plates, priority_samples, mocked_responses, mlwh_lh_samples, endpoint
):
    body = create_plate_body(VALID_PLATE_BARCODE, "all_samples")
    mock_labware_lookup(app, mocked_responses)
    mock_plate_create(app, mocked_responses, body)

    response = client.post(endpoint, json=body)

    assert response.status_code == HTTPStatus.CREATED

    # There are 8 samples on the plate. No filters are made on the samples before they are returned.
    assert response.json == {"data": {"plate_barcode": VALID_PLATE_BARCODE, "centre": "centre_1", "count_samples": 8}}


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
def test_post_plates_endpoint_successful_with_all_new_samples_only_plate_type_and_all_cog_barcodes_already_in_samples(
    app, client, samples, source_plates, priority_samples, mocked_responses, mlwh_lh_samples, endpoint
):
    body = create_plate_body(VALID_PLATE_BARCODE, "all_new_samples_only")
    mock_labware_lookup(app, mocked_responses)
    mock_samples_lookup(app, mocked_responses)
    mock_plate_create(app, mocked_responses, body)

    response = client.post(endpoint, json=body)

    assert response.status_code == HTTPStatus.CREATED

    # There are 8 samples on the plate. No filters are made on the samples before they are returned.
    assert response.json == {"data": {"plate_barcode": VALID_PLATE_BARCODE, "centre": "centre_1", "count_samples": 8}}


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
def test_post_plates_endpoint_successful_with_all_new_samples_only_plate_type_some_samples_already_in_ss(
    app, client, samples, source_plates, priority_samples, mocked_responses, mlwh_lh_samples, endpoint
):
    body = create_plate_body(VALID_PLATE_BARCODE, "all_new_samples_only")
    mock_labware_lookup(app, mocked_responses)
    mock_samples_lookup(app, mocked_responses, found_samples_count=5)
    mock_plate_create(app, mocked_responses, body)

    response = client.post(endpoint, json=body)

    assert response.status_code == HTTPStatus.CREATED

    # There are 8 samples on the plate. 5 samples already exist in Sequencescape.
    assert response.json == {"data": {"plate_barcode": VALID_PLATE_BARCODE, "centre": "centre_1", "count_samples": 3}}


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
def test_post_plates_endpoint_successful_with_all_new_samples_only_plate_type_all_samples_already_in_ss(
    app, client, samples, source_plates, priority_samples, mocked_responses, mlwh_lh_samples, endpoint
):
    body = create_plate_body(VALID_PLATE_BARCODE, "all_new_samples_only")
    mock_labware_lookup(app, mocked_responses)
    mock_samples_lookup(app, mocked_responses, found_samples_count=8, mock_missing_samples=False)

    response = client.post(endpoint, json=body)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": [f"No samples found on plate with barcode: {VALID_PLATE_BARCODE}"]}


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
def test_post_plates_endpoint_no_barcode_in_request(app, client, endpoint):
    response = client.post(endpoint, json={})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["POST request needs 'barcode' in body"]}


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
def test_post_plates_endpoint_plate_type_not_configured(app, client, endpoint):
    response = client.post(endpoint, json={QUERY_PARAM_BARCODE: "plate_123", "type": "bogus"})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {
        "errors": [
            (
                "POST request 'type' must be from the list: "
                "heron, fit_to_pick_new_samples_only, all_samples, all_new_samples_only"
            )
        ]
    }


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
@pytest.mark.parametrize("plate_type", ALL_SAMPLES_PLATE_TYPES)
def test_post_plates_endpoint_exception_for_all_samples_plate_type_when_plate_already_in_ss(
    app, client, source_plates, mocked_responses, endpoint, plate_type
):
    body = create_plate_body(VALID_PLATE_BARCODE, plate_type)
    mock_labware_lookup(app, mocked_responses, labware_found_count=1)

    response = client.post(endpoint, json=body)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": [f"The barcode '{VALID_PLATE_BARCODE}' is already in use."]}


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
@pytest.mark.parametrize("plate_type", FIT_TO_PICK_PLATE_TYPES)
def test_post_plates_endpoint_fit_to_pick_plate_type_no_fit_to_pick_samples(
    app, client, samples, source_plates, endpoint, plate_type
):
    body = create_plate_body(INVALID_PLATE_BARCODE, plate_type)

    response = client.post(endpoint, json=body)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": [f"No fit to pick samples for this barcode: {INVALID_PLATE_BARCODE}"]}


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
@pytest.mark.parametrize("plate_type", ALL_SAMPLES_PLATE_TYPES)
def test_post_plates_endpoint_all_samples_plate_type_barcode_does_not_exist(
    app, client, samples, source_plates, endpoint, plate_type
):
    body = create_plate_body(INVALID_PLATE_BARCODE, plate_type)

    response = client.post(endpoint, json=body)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": [f"No plate exists for barcode: {INVALID_PLATE_BARCODE}"]}


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
@pytest.mark.parametrize("plate_type", ALL_SAMPLES_PLATE_TYPES)
def test_post_plates_endpoint_all_samples_plate_type_no_samples(
    app, mocked_responses, client, samples, source_plates, endpoint, plate_type
):
    body = create_plate_body(EMPTY_PLATE_BARCODE, plate_type)
    mock_labware_lookup(app, mocked_responses)  # The check for samples comes after checking the plate exists

    response = client.post(endpoint, json=body)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": [f"No samples found on plate with barcode: {EMPTY_PLATE_BARCODE}"]}


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
@pytest.mark.parametrize("plate_type", FIT_TO_PICK_PLATE_TYPES)
def test_post_plates_endpoint_fit_to_pick_type_with_ss_create_failure(
    app, client, samples, source_plates, mocked_responses, endpoint, plate_type
):
    mock_plate_create(app, mocked_responses)

    body = create_plate_body(VALID_PLATE_BARCODE, plate_type)

    response = client.post(endpoint, json=body)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == CREATE_PLATE_ERROR_JSON


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
@pytest.mark.parametrize("plate_type", ALL_SAMPLES_PLATE_TYPES)
def test_post_plates_endpoint_all_samples_type_with_ss_plate_lookup_failure(
    app, client, source_plates, mocked_responses, endpoint, plate_type
):
    mock_labware_lookup_failure(app, mocked_responses)

    body = create_plate_body(VALID_PLATE_BARCODE, plate_type)

    response = client.post(endpoint, json=body)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == {
        "errors": ["An unexpected error occurred attempting to create a plate in Sequencescape: (AssertionError)"]
    }


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
def test_post_plates_endpoint_all_samples_type_with_ss_failure(
    app, client, samples, source_plates, mocked_responses, endpoint
):
    mock_labware_lookup(app, mocked_responses)
    mock_plate_create(app, mocked_responses)

    body = create_plate_body(VALID_PLATE_BARCODE, "all_samples")

    response = client.post(endpoint, json=body)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == CREATE_PLATE_ERROR_JSON


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
def test_post_plates_endpoint_all_new_samples_only_type_with_ss_samples_lookup_failure(
    app, client, samples, source_plates, mocked_responses, endpoint
):
    mock_labware_lookup(app, mocked_responses)
    mock_samples_lookup_failure(app, mocked_responses)

    body = create_plate_body(VALID_PLATE_BARCODE, "all_new_samples_only")

    response = client.post(endpoint, json=body)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == {
        "errors": ["An unexpected error occurred attempting to create a plate in Sequencescape: (ConnectionError)"]
    }


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
def test_post_plates_endpoint_all_new_samples_only_type_with_ss_failure(
    app, client, samples, source_plates, mocked_responses, endpoint
):
    mock_labware_lookup(app, mocked_responses)
    mock_samples_lookup(app, mocked_responses)
    mock_plate_create(app, mocked_responses)

    body = create_plate_body(VALID_PLATE_BARCODE, "all_new_samples_only")

    response = client.post(endpoint, json=body)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == CREATE_PLATE_ERROR_JSON


@pytest.mark.parametrize("endpoint", GET_PLATES_ENDPOINTS)
def test_get_plates_endpoint_successful(
    app, client, samples, priority_samples, mocked_responses, plates_lookup_without_samples, endpoint
):
    params = {QUERY_PARAM_BARCODES: "plate_123,456", ARG_EXCLUDE: "pickable_samples"}
    response = client.get(endpoint, query_string=params, content_type="application/json")

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "plates": [
            plates_lookup_without_samples["plate_123"],
            {
                "plate_barcode": "456",
                "has_plate_map": False,
                "count_fit_to_pick_samples": 0,
                "count_filtered_positive": 0,
                "count_must_sequence": 0,
                "count_preferentially_sequence": 0,
            },
        ]
    }

    params = {QUERY_PARAM_BARCODES: "456", ARG_EXCLUDE: "pickable_samples", ARG_TYPE: ARG_TYPE_SOURCE}
    response = client.get(endpoint, query_string=params)

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "plates": [
            {
                "plate_barcode": "456",
                "has_plate_map": False,
                "count_fit_to_pick_samples": 0,
                "count_filtered_positive": 0,
                "count_must_sequence": 0,
                "count_preferentially_sequence": 0,
            },
        ]
    }


@pytest.mark.parametrize("endpoint", GET_PLATES_ENDPOINTS)
def test_get_plates_endpoint_no_barcode_in_request(client, endpoint):
    response = client.get(endpoint)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize("endpoint", GET_PLATES_ENDPOINTS)
def test_get_plates_endpoint_barcode_empty(client, endpoint):
    response = client.get(endpoint, query_string={QUERY_PARAM_BARCODES: ""})

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize("endpoint", GET_PLATES_ENDPOINTS)
def test_get_plates_endpoint_method_calls(app, client, samples, priority_samples, endpoint):
    barcode = "plate_123"
    with patch("lighthouse.helpers.plates.has_plate_map_data", return_value=True) as mock_has_plate_map_data:
        response = client.get(endpoint, query_string={QUERY_PARAM_BARCODES: barcode}, content_type="application/json")
        assert response.status_code == HTTPStatus.OK
        mock_has_plate_map_data.assert_called_once_with(barcode)


@pytest.mark.parametrize("endpoint", GET_PLATES_ENDPOINTS)
def test_get_plates_endpoint_fail(app, client, samples, mocked_responses, endpoint):
    with patch("lighthouse.helpers.plates.get_fit_to_pick_samples_and_counts", side_effect=Exception()):
        response = client.get(endpoint, query_string={QUERY_PARAM_BARCODES: "123,456"}, content_type="application/json")

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert response.json == {"errors": ["Failed to lookup plates: Exception"]}


@pytest.mark.parametrize("endpoint", GET_PLATES_ENDPOINTS)
def test_get_plates_endpoint_exclude_props(
    app, client, samples, priority_samples, mocked_responses, plates_lookup_with_samples, endpoint
):
    params = {QUERY_PARAM_BARCODES: "plate_123,456", ARG_EXCLUDE: "plate_barcode"}
    response = client.get(endpoint, query_string=params)

    assert response.status_code == HTTPStatus.OK

    # shallow copy of plate
    first_plate = plates_lookup_with_samples["plate_123"].copy()
    # we remove the barcode attr
    first_plate.pop("plate_barcode")

    assert response.json == {
        "plates": [
            first_plate,
            {
                "has_plate_map": False,
                "count_fit_to_pick_samples": 0,
                "count_filtered_positive": 0,
                "count_must_sequence": 0,
                "count_preferentially_sequence": 0,
                "pickable_samples": [],
            },
        ]
    }


@pytest.mark.parametrize("endpoint", GET_PLATES_ENDPOINTS)
def test_get_plates_with_type(app, client, mocked_responses, endpoint):
    ss_url = f"{app.config['SS_URL']}/api/v2/labware"
    first_plate_barcode = "plate_123"
    second_plate_barcode = "plate_456"

    first_plate_params = {"filter[barcode]": first_plate_barcode}
    mocked_responses.add(
        responses.GET,
        ss_url,
        json={"data": ["barcode exists!"]},
        status=HTTPStatus.OK,
        match=[query_param_matcher(first_plate_params)],
    )

    second_plate_params = {"filter[barcode]": second_plate_barcode}
    mocked_responses.add(
        responses.GET,
        ss_url,
        json={"data": []},
        status=HTTPStatus.OK,
        match=[query_param_matcher(second_plate_params)],
    )

    params = {QUERY_PARAM_BARCODES: f"{first_plate_barcode},{second_plate_barcode}", ARG_TYPE: ARG_TYPE_DESTINATION}
    response = client.get(endpoint, query_string=params)

    assert response.status_code == HTTPStatus.OK

    assert response.json == {
        "plates": [
            {
                "plate_barcode": first_plate_barcode,
                "plate_exists": True,
            },
            {
                "plate_barcode": second_plate_barcode,
                "plate_exists": False,
            },
        ]
    }


@pytest.mark.parametrize("endpoint", GET_PLATES_ENDPOINTS)
def test_get_plates_with_invalid_type(app, client, endpoint):
    params = {QUERY_PARAM_BARCODES: "plate_123,plate_456", ARG_TYPE: "invalid_type"}
    response = client.get(endpoint, query_string=params)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize("endpoint", CHERRYTRACK_PLATES_ENDPOINT)
def test_get_cherrytrack_plates_source_endpoint_successful(app, client, mocked_responses, endpoint):
    plate_barcode = "cherrytrack_plate_123"
    cherrytrack_url = f"{app.config['CHERRYTRACK_URL']}/source-plates/{plate_barcode}"
    body = {
        "data": {
            "barcode": "cherrytrack_plate_123",
            "samples": [
                {
                    "automation_system_run_id": "",
                    "created_at": "Wed, 27 Oct 2021 09:04:49 GMT",
                    "date_picked": "",
                    "destination_barcode": "",
                    "destination_coordinate": "",
                    "lab_id": "MK",
                    "lh_sample_uuid": "6d0da56a-2f4c-4f4a-bb21-47f568abfbaa",
                    "picked": "false",
                    "rna_id": "RNA-S-00001-00000007",
                    "source_barcode": "DS000010001",
                    "source_coordinate": "A11",
                    "type": "sample",
                }
            ],
        }
    }
    mocked_responses.add(responses.GET, cherrytrack_url, json=body, status=HTTPStatus.OK)

    params = {QUERY_PARAM_BARCODE: plate_barcode, ARG_TYPE: "source"}
    response = client.get(endpoint, query_string=params)

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"plate": body}


@pytest.mark.parametrize("endpoint", CHERRYTRACK_PLATES_ENDPOINT)
def test_get_cherrytrack_plates_destination_endpoint_successful(app, client, mocked_responses, endpoint):
    plate_barcode = "cherrytrack_plate_123"
    cherrytrack_url = f"{app.config['CHERRYTRACK_URL']}/destination-plates/{plate_barcode}"
    body = {
        "data": {
            "barcode": "cherrytrack_plate_123",
            "samples": [
                {
                    "automation_system_run_id": 1,
                    "created_at": "Wed, 27 Oct 2021 09:04:49 GMT",
                    "date_picked": "Wed, 27 Oct 2021 09:04:50 GMT",
                    "destination_barcode": "DN00000001",
                    "destination_coordinate": "B6",
                    "lab_id": "MK",
                    "lh_sample_uuid": "01d543f4-0922-4a5d-b026-856cc429d4c6",
                    "picked": "true",
                    "rna_id": "RNA-S-00001-00000018",
                    "source_barcode": "DS000010001",
                    "source_coordinate": "B3",
                    "type": "sample",
                }
            ],
        }
    }
    mocked_responses.add(responses.GET, cherrytrack_url, json=body, status=HTTPStatus.OK)

    params = {QUERY_PARAM_BARCODE: plate_barcode, ARG_TYPE: "destination"}
    response = client.get(endpoint, query_string=params)

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"plate": body}


@pytest.mark.parametrize("endpoint", CHERRYTRACK_PLATES_ENDPOINT)
def test_get_cherrytrack_plates_endpoint_empty_barcode(app, client, endpoint):
    params = {QUERY_PARAM_BARCODE: "", ARG_TYPE: "destination"}
    response = client.get(endpoint, query_string=params)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["Include a barcode in the request"]}


@pytest.mark.parametrize("endpoint", CHERRYTRACK_PLATES_ENDPOINT)
def test_get_cherrytrack_plates_endpoint_empty_type(app, client, endpoint):
    params = {QUERY_PARAM_BARCODE: "cherrytrack_plate_123", ARG_TYPE: ""}
    response = client.get(endpoint, query_string=params)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["Plate type needs to be either 'source' or 'destination'"]}


@pytest.mark.parametrize("endpoint", CHERRYTRACK_PLATES_ENDPOINT)
def test_get_cherrytrack_plates_endpoint_failure(app, client, mocked_responses, endpoint):
    plate_barcode = "cherrytrack_plate_123"
    cherrytrack_url = f"{app.config['CHERRYTRACK_URL']}/destination-plates/{plate_barcode}"
    body = {"errors": ["Failed to get source plate info: Failed to find samples for source plate barcode DS0000100"]}
    mocked_responses.add(responses.GET, cherrytrack_url, json=body, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    params = {QUERY_PARAM_BARCODE: plate_barcode, ARG_TYPE: "destination"}
    response = client.get(endpoint, query_string=params)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == {
        "errors": ["Failed to get source plate info: Failed to find samples for source plate barcode DS0000100"]
    }
