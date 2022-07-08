import json
import string
from http import HTTPStatus
from unittest.mock import patch

import pytest
import responses

from lighthouse.constants.error_messages import (
    ERROR_SAMPLE_DATA_MISMATCH,
    ERROR_SAMPLE_DATA_MISSING,
    ERROR_SAMPLES_MISSING_UUIDS,
    ERROR_UNEXPECTED_CHERRYPICKING_FAILURE,
    ERROR_UPDATE_MLWH_WITH_COG_UK_IDS,
)
from lighthouse.constants.fields import FIELD_COG_BARCODE, FIELD_ROOT_SAMPLE_ID
from lighthouse.messages.message import Message

ENDPOINT_PREFIXES = ["", "/v1"]
CREATE_PLATE_ENDPOINT = "/cherrypicked-plates/create"
FAIL_PLATE_ENDPOINT = "/cherrypicked-plates/fail"

CREATE_PLATE_BASE_URLS = [prefix + CREATE_PLATE_ENDPOINT for prefix in ENDPOINT_PREFIXES]
FAIL_PLATE_BASE_URLS = [prefix + FAIL_PLATE_ENDPOINT for prefix in ENDPOINT_PREFIXES]


@pytest.fixture
def samples_with_cog_barcodes(samples):
    samples, _ = samples
    return [sample for sample in samples if FIELD_COG_BARCODE in sample]


# ---------- cherrypicked-plates/create tests ----------


def unique_barcodes(count):
    return [string.ascii_lowercase[i : i + 3] for i in range(count)]  # noqa: E203


def mock_baracoda(mocked_responses, app, barcodes, bad_request=False):
    url = f"{app.config['BARACODA_URL']}/barcodes_group/TC1/new?count={len(barcodes)}"
    body = json.dumps({"barcodes_group": {"barcodes": barcodes}})
    status = HTTPStatus.BAD_REQUEST if bad_request else HTTPStatus.CREATED

    mocked_responses.add(responses.POST, url, body=body, status=status)


def mock_sequencescape(mocked_responses, app, bad_request_barcode=None):
    ss_url = f"{app.config['SS_URL']}/api/v2/heron/plates"
    json_body: dict = (
        {"errors": [f"The barcode '{bad_request_barcode}' is not a recognised format."]}
        if bad_request_barcode
        else {"barcode": "des_plate_1"}
    )
    status = HTTPStatus.UNPROCESSABLE_ENTITY if bad_request_barcode else HTTPStatus.OK

    mocked_responses.add(
        responses.POST,
        ss_url,
        json=json_body,
        status=status,
    )


@pytest.mark.parametrize("base_url", CREATE_PLATE_BASE_URLS)
def test_get_cherrypicked_plates_endpoint_successful(
    app,
    client,
    dart_samples,
    samples_with_cog_barcodes,
    mocked_responses,
    centres,
    mlwh_lh_samples,
    source_plates,
    base_url,
):
    mock_baracoda(mocked_responses, app, unique_barcodes(2))
    mock_sequencescape(mocked_responses, app)

    response = client.get(
        f"{base_url}?barcode=des_plate_1&robot=BKRB0001&user_id=test", content_type="application/json"
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "data": {"plate_barcode": "des_plate_1", "centre": ["centre_1"], "number_of_fit_to_pick": 5}
    }


@pytest.mark.parametrize("base_url", CREATE_PLATE_BASE_URLS)
def test_get_cherrypicked_plates_endpoint_only_updated_correct_samples_in_mlwh(
    app,
    client,
    dart_samples,
    samples,
    mocked_responses,
    centres,
    mlwh_lh_samples,
    source_plates,
    base_url,
):
    barcodes = unique_barcodes(2)
    mock_baracoda(mocked_responses, app, barcodes)
    mock_sequencescape(mocked_responses, app)

    all_samples, _ = samples
    sample004 = next(s for s in all_samples if s[FIELD_ROOT_SAMPLE_ID] == "sample_004")
    sample005 = next(s for s in all_samples if s[FIELD_ROOT_SAMPLE_ID] == "sample_005")

    # Check these samples have the COG UK IDs expected to be updatable
    assert FIELD_COG_BARCODE in sample004 and sample004[FIELD_COG_BARCODE] == ""
    assert FIELD_COG_BARCODE not in sample005

    with patch("lighthouse.routes.common.cherrypicked_plates.update_mlwh_with_cog_uk_ids") as update_mlwh:
        client.get(f"{base_url}?barcode=des_plate_1&robot=BKRB0001&user_id=test", content_type="application/json")

    update_mlwh.assert_called_once()

    updated_samples = update_mlwh.call_args.args[0]
    updated_sample004 = next(s for s in updated_samples if s[FIELD_ROOT_SAMPLE_ID] == "sample_004")
    updated_sample005 = next(s for s in updated_samples if s[FIELD_ROOT_SAMPLE_ID] == "sample_005")

    assert len(updated_samples) == 2
    assert updated_sample004[FIELD_COG_BARCODE] in barcodes
    assert updated_sample005[FIELD_COG_BARCODE] in barcodes
    assert updated_sample004[FIELD_COG_BARCODE] != updated_sample005[FIELD_COG_BARCODE]


@pytest.mark.parametrize("base_url", CREATE_PLATE_BASE_URLS)
def test_get_cherrypicked_plates_endpoint_no_barcode_in_request(app, client, samples, base_url):
    response = client.get(f"{base_url}?user_id=test&robot=BKRB0001", content_type="application/json")

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["GET request needs 'barcode' in URL"]}


@pytest.mark.parametrize("base_url", CREATE_PLATE_BASE_URLS)
def test_get_cherrypicked_plates_endpoint_no_robot_number_in_request(app, client, samples, base_url):
    response = client.get(
        f"{base_url}?barcode=plate_1&user_id=test",
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["GET request needs 'robot' in URL"]}


@pytest.mark.parametrize("base_url", CREATE_PLATE_BASE_URLS)
def test_get_cherrypicked_plates_endpoint_no_user_id_in_request(app, client, samples, base_url):
    response = client.get(
        f"{base_url}?barcode=plate_1&robot=1234",
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["GET request needs 'user_id' in URL"]}


@pytest.mark.parametrize("base_url", CREATE_PLATE_BASE_URLS)
def test_get_cherrypicked_plates_endpoint_add_cog_barcodes_failed(
    app,
    client,
    dart_samples,
    samples,
    centres,
    mocked_responses,
    base_url,
):
    mock_baracoda(mocked_responses, app, unique_barcodes(2), bad_request=True)

    barcode = "des_plate_1"
    response = client.get(
        f"{base_url}?barcode={barcode}&robot=BKRB0001&user_id=test",
        content_type="application/json",
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": [f"Failed to add COG barcodes to plate: {barcode}"]}


@pytest.mark.parametrize("base_url", CREATE_PLATE_BASE_URLS)
def test_get_cherrypicked_plates_endpoint_ss_failure(
    app,
    client,
    dart_samples,
    samples,
    centres,
    mocked_responses,
    source_plates,
    base_url,
):
    barcode = "des_plate_1"

    mock_baracoda(mocked_responses, app, unique_barcodes(2))
    mock_sequencescape(mocked_responses, app, barcode)

    response = client.get(
        f"{base_url}?barcode={barcode}&robot=BKRB0001&user_id=test",
        content_type="application/json",
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == {"errors": [f"The barcode '{barcode}' is not a recognised format."]}


@pytest.mark.parametrize("base_url", CREATE_PLATE_BASE_URLS)
def test_get_cherrypicked_plates_mlwh_update_failure(
    app,
    client,
    dart_samples,
    centres,
    samples,
    mocked_responses,
    source_plates,
    base_url,
):
    mock_baracoda(mocked_responses, app, unique_barcodes(2))
    mock_sequencescape(mocked_responses, app)

    with patch(
        "lighthouse.routes.common.cherrypicked_plates.update_mlwh_with_cog_uk_ids",
        side_effect=Exception(),
    ):
        response = client.get(
            f"{base_url}?barcode=des_plate_1&robot=BKRB0001&user_id=test",
            content_type="application/json",
        )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == {
        "errors": [
            (
                "Failed to update MLWH with COG UK ids. The samples should have been "
                "successfully inserted into Sequencescape."
            )
        ]
    }

    assert response.json == {"errors": [ERROR_UPDATE_MLWH_WITH_COG_UK_IDS]}


@pytest.mark.parametrize("base_url", CREATE_PLATE_BASE_URLS)
def test_post_plates_endpoint_mismatched_sample_numbers(app, client, dart_samples, samples, base_url):
    with patch(
        "lighthouse.routes.common.cherrypicked_plates.add_cog_barcodes_from_different_centres",
        return_value="TC1",
    ):
        with patch(
            "lighthouse.routes.common.cherrypicked_plates.check_matching_sample_numbers",
            return_value=False,
        ):
            barcode = "des_plate_1"
            response = client.get(
                f"{base_url}?barcode={barcode}&robot=BKRB0001&user_id=test",
                content_type="application/json",
            )

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert response.json == {"errors": [f"{ERROR_SAMPLE_DATA_MISMATCH} {barcode}"]}


@pytest.mark.parametrize("base_url", CREATE_PLATE_BASE_URLS)
def test_post_cherrypicked_plates_endpoint_missing_dart_data(app, client, base_url):
    with patch("lighthouse.routes.common.cherrypicked_plates.find_dart_source_samples_rows", return_value=[]):
        barcode = "des_plate_1"
        response = client.get(
            f"{base_url}?barcode={barcode}&robot=BKRB0001&user_id=test",
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert response.json == {"errors": [f"{ERROR_SAMPLE_DATA_MISSING} {barcode}"]}


@pytest.mark.parametrize("base_url", CREATE_PLATE_BASE_URLS)
def test_post_cherrypicked_plates_endpoint_missing_source_plate_uuids(
    app, client, dart_samples, samples, centres, mocked_responses, base_url
):
    mock_baracoda(mocked_responses, app, unique_barcodes(2))

    barcode = "des_plate_1"

    with patch(
        "lighthouse.routes.common.cherrypicked_plates.get_source_plates_for_samples",
        return_value=[],
    ):
        response = client.get(
            f"{base_url}?barcode={barcode}&robot=BKRB0001&user_id=test",
            content_type="application/json",
        )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": [f"{ERROR_SAMPLES_MISSING_UUIDS} {barcode}"]}


# ---------- cherrypicked-plates/fail tests ----------


@pytest.mark.parametrize("base_url", FAIL_PLATE_BASE_URLS)
def test_fail_plate_from_barcode_bad_request_no_barcode(client, base_url):
    response = client.get(f"{base_url}?user_id=test_user&robot=BKRB0001&failure_type=robot_crashed")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1

    response = client.get(f"{base_url}?user_id=test_user&robot=BKRB0001" "&failure_type=robot_crashed&barcode=")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1


@pytest.mark.parametrize("base_url", FAIL_PLATE_BASE_URLS)
def test_fail_plate_from_barcode_bad_request_no_user_id(client, base_url):
    response = client.get(f"{base_url}?barcode=ABC123&robot=BKRB0001&failure_type=robot_crashed")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1

    response = client.get(f"{base_url}?barcode=ABC123&robot=BKRB0001" "&failure_type=robot_crashed&user_id=")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1


@pytest.mark.parametrize("base_url", FAIL_PLATE_BASE_URLS)
def test_fail_plate_from_barcode_bad_request_no_robot(client, base_url):
    response = client.get(f"{base_url}?barcode=ABC123&user_id=test_user&failure_type=robot_crashed")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1

    response = client.get(f"{base_url}?barcode=ABC123&user_id=test_user" "&failure_type=robot_crashed&robot=")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1


@pytest.mark.parametrize("base_url", FAIL_PLATE_BASE_URLS)
def test_fail_plate_from_barcode_bad_request_no_failure_type(client, base_url):
    response = client.get(f"{base_url}?barcode=ABC123&user_id=test_user&robot=BKRB0001")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1

    response = client.get(f"{base_url}?barcode=ABC123&user_id=test_user&robot=BKRB0001&failure_type=")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1


@pytest.mark.parametrize("base_url", FAIL_PLATE_BASE_URLS)
def test_fail_plate_from_barcode_bad_request_unrecognised_failure_type(app, client, base_url):
    with app.app_context():
        failure_type = "notAFailureType"
        response = client.get(
            f"{base_url}?barcode=ABC123&user_id=test_user" f"&robot=BKRB0001&failure_type={failure_type}"
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert f"'{failure_type}' is not a known cherrypicked plate failure type" in response.json["errors"]


@pytest.mark.parametrize("base_url", FAIL_PLATE_BASE_URLS)
def test_fail_plate_from_barcode_internal_server_error_constructing_message_failure(app, client, base_url):
    with app.app_context():
        with patch(
            "lighthouse.routes.common.cherrypicked_plates.construct_cherrypicking_plate_failed_message",
            side_effect=Exception(),
        ):
            response = client.get(
                f"{base_url}?barcode=ABC123&user_id=test_user" "&robot=BKRB0001&failure_type=robot_crashed"
            )
            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert ERROR_UNEXPECTED_CHERRYPICKING_FAILURE in response.json["errors"][0]


@pytest.mark.parametrize("base_url", FAIL_PLATE_BASE_URLS)
def test_fail_plate_from_barcode_internal_server_error_constructing_message_none(app, client, base_url):
    with app.app_context():
        test_error = "this is a test error"
        with patch(
            "lighthouse.routes.common.cherrypicked_plates.construct_cherrypicking_plate_failed_message",
            return_value=([test_error], None),
        ):
            response = client.get(
                f"{base_url}?barcode=ABC123&user_id=test_user&robot=BKRB0001&failure_type=robot_crashed"
            )
            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert test_error in response.json["errors"][0]


@pytest.mark.parametrize("base_url", FAIL_PLATE_BASE_URLS)
def test_fail_plate_from_barcode_internal_error_failed_broker_initialise(client, base_url):
    with patch(
        "lighthouse.routes.common.cherrypicked_plates.construct_cherrypicking_plate_failed_message"
    ) as mock_construct:
        with patch("lighthouse.routes.common.cherrypicked_plates.Broker", side_effect=Exception()):
            mock_construct.return_value = [], Message({"test": "me"})

            response = client.get(
                f"{base_url}?barcode=plate_1&user_id=test_user" "&robot=BKRB0001&failure_type=robot_crashed"
            )

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert ERROR_UNEXPECTED_CHERRYPICKING_FAILURE in response.json["errors"][0]


@pytest.mark.parametrize("base_url", FAIL_PLATE_BASE_URLS)
def test_fail_plate_from_barcode_internal_error_failed_broker_connect(client, base_url):
    with patch(
        "lighthouse.routes.common.cherrypicked_plates.construct_cherrypicking_plate_failed_message"
    ) as mock_construct:
        with patch("lighthouse.routes.common.cherrypicked_plates.Broker._connect", side_effect=Exception()):
            mock_construct.return_value = [], Message({"test": "me"})

            response = client.get(
                f"{base_url}?barcode=plate_1&user_id=test_user" "&robot=BKRB0001&failure_type=robot_crashed"
            )

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert ERROR_UNEXPECTED_CHERRYPICKING_FAILURE in response.json["errors"][0]


@pytest.mark.parametrize("base_url", FAIL_PLATE_BASE_URLS)
def test_fail_plate_from_barcode_internal_error_failed_broker_publish(client, base_url):
    with patch(
        "lighthouse.routes.common.cherrypicked_plates.construct_cherrypicking_plate_failed_message"
    ) as mock_construct:
        with patch("lighthouse.routes.common.cherrypicked_plates.Broker") as mock_broker:
            mock_broker().publish.side_effect = Exception()
            mock_construct.return_value = [], Message({"test": "me"})

            response = client.get(
                f"{base_url}?barcode=plate_1&user_id=test_user" "&robot=BKRB0001&failure_type=robot_crashed"
            )

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert ERROR_UNEXPECTED_CHERRYPICKING_FAILURE in response.json["errors"][0]


@pytest.mark.parametrize("base_url", FAIL_PLATE_BASE_URLS)
def test_fail_plate_from_barcode_success(client, base_url):
    with patch(
        "lighthouse.routes.common.cherrypicked_plates.construct_cherrypicking_plate_failed_message"
    ) as mock_construct:
        routing_key = "test.routing.key"
        with patch("lighthouse.routes.common.cherrypicked_plates.get_routing_key", return_value=routing_key):
            with patch("lighthouse.routes.common.cherrypicked_plates.Broker") as mock_broker:
                test_errors = ["error 1", "error 2"]
                test_message = Message({"test": "me"})
                mock_construct.return_value = test_errors, test_message

                response = client.get(
                    f"{base_url}?barcode=plate_1&user_id=test_user" "&robot=BKRB0001&failure_type=robot_crashed"
                )

                mock_broker().publish.assert_called_with(test_message, routing_key)
                mock_broker()._close_connection.assert_called()
                assert response.status_code == HTTPStatus.OK
                assert response.json["errors"] == test_errors
