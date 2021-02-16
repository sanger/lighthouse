from http import HTTPStatus
from unittest.mock import patch

import responses

from lighthouse.constants.error_messages import (
    ERROR_SAMPLE_DATA_MISMATCH,
    ERROR_SAMPLE_DATA_MISSING,
    ERROR_SAMPLES_MISSING_UUIDS,
    ERROR_UNEXPECTED_CHERRYPICKING_FAILURE,
    ERROR_UPDATE_MLWH_WITH_COG_UK_IDS,
)
from lighthouse.messages.message import Message

# ---------- cherrypicked-plates/create tests ----------


def test_get_cherrypicked_plates_endpoint_successful(
    app,
    client,
    dart_samples,
    samples,
    mocked_responses,
    mlwh_lh_samples,
    source_plates,
):
    with patch(
        "lighthouse.blueprints.cherrypicked_plates.add_cog_barcodes",
        return_value="TC1",
    ):
        ss_url = f"http://{app.config['SS_HOST']}/api/v2/heron/plates"

        mocked_responses.add(
            responses.POST,
            ss_url,
            json={"barcode": "des_plate_1"},
            status=HTTPStatus.OK,
        )
        response = client.get(
            "/cherrypicked-plates/create?barcode=des_plate_1&robot=BKRB0001&user_id=test",
            content_type="application/json",
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json == {"data": {"plate_barcode": "des_plate_1", "centre": "TC1", "number_of_positives": 5}}


def test_get_cherrypicked_plates_endpoint_no_barcode_in_request(app, client, samples):
    response = client.get("/cherrypicked-plates/create?user_id=test&robot=BKRB0001", content_type="application/json")

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["GET request needs 'barcode' in URL"]}


def test_get_cherrypicked_plates_endpoint_no_robot_number_in_request(app, client, samples):
    response = client.get(
        "/cherrypicked-plates/create?barcode=plate_1&user_id=test",
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["GET request needs 'robot' in URL"]}


def test_get_cherrypicked_plates_endpoint_no_user_id_in_request(app, client, samples):
    response = client.get(
        "/cherrypicked-plates/create?barcode=plate_1&robot=1234",
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["GET request needs 'user_id' in URL"]}


def test_get_cherrypicked_plates_endpoint_add_cog_barcodes_failed(
    app, client, dart_samples, samples, centres, mocked_responses
):
    baracoda_url = f"http://{app.config['BARACODA_URL']}/barcodes_group/TC1/new?count=5"

    mocked_responses.add(
        responses.POST,
        baracoda_url,
        status=HTTPStatus.BAD_REQUEST,
    )
    barcode = "des_plate_1"
    response = client.get(
        f"/cherrypicked-plates/create?barcode={barcode}&robot=BKRB0001&user_id=test",
        content_type="application/json",
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": [f"Failed to add COG barcodes to plate: {barcode}"]}


def test_get_cherrypicked_plates_endpoint_ss_failure(
    app, client, dart_samples, samples, mocked_responses, source_plates
):
    with patch("lighthouse.blueprints.cherrypicked_plates.add_cog_barcodes", return_value="TC1"):
        ss_url = f"http://{app.config['SS_HOST']}/api/v2/heron/plates"

        barcode = "des_plate_1"
        body = {"errors": [f"The barcode '{barcode}' is not a recognised format."]}
        mocked_responses.add(
            responses.POST,
            ss_url,
            json=body,
            status=HTTPStatus.UNPROCESSABLE_ENTITY,
        )

        response = client.get(
            f"/cherrypicked-plates/create?barcode={barcode}&robot=BKRB0001&user_id=test",
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json == {"errors": [f"The barcode '{barcode}' is not a recognised format."]}


def test_get_cherrypicked_plates_mlwh_update_failure(
    app, client, dart_samples, samples, mocked_responses, source_plates
):
    with patch("lighthouse.blueprints.cherrypicked_plates.add_cog_barcodes", return_value="TC1"):
        with patch("lighthouse.blueprints.cherrypicked_plates.update_mlwh_with_cog_uk_ids", side_effect=Exception()):
            ss_url = f"http://{app.config['SS_HOST']}/api/v2/heron/plates"
            body = {"barcode": "plate_1"}

            mocked_responses.add(
                responses.POST,
                ss_url,
                json=body,
                status=HTTPStatus.OK,
            )

            response = client.get(
                "/cherrypicked-plates/create?barcode=des_plate_1&robot=BKRB0001&user_id=test",
                content_type="application/json",
            )

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert response.json == {"errors": [ERROR_UPDATE_MLWH_WITH_COG_UK_IDS]}


def test_post_plates_endpoint_mismatched_sample_numbers(app, client, dart_samples, samples):
    with patch("lighthouse.blueprints.cherrypicked_plates.add_cog_barcodes", return_value="TC1"):
        with patch("lighthouse.blueprints.cherrypicked_plates.check_matching_sample_numbers", return_value=False):
            barcode = "des_plate_1"
            response = client.get(
                f"/cherrypicked-plates/create?barcode={barcode}&robot=BKRB0001&user_id=test",
                content_type="application/json",
            )

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert response.json == {"errors": [f"{ERROR_SAMPLE_DATA_MISMATCH} {barcode}"]}


def test_post_cherrypicked_plates_endpoint_missing_dart_data(app, client):
    with patch("lighthouse.blueprints.cherrypicked_plates.find_dart_source_samples_rows", return_value=[]):
        barcode = "des_plate_1"
        response = client.get(
            f"/cherrypicked-plates/create?barcode={barcode}&robot=BKRB0001&user_id=test",
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert response.json == {"errors": [f"{ERROR_SAMPLE_DATA_MISSING} {barcode}"]}


def test_post_cherrypicked_plates_endpoint_missing_source_plate_uuids(app, client, dart_samples, samples):
    with patch("lighthouse.blueprints.cherrypicked_plates.add_cog_barcodes", return_value="TC1"):
        with patch("lighthouse.blueprints.cherrypicked_plates.get_source_plates_for_samples", return_value=[]):
            barcode = "des_plate_1"
            response = client.get(
                f"/cherrypicked-plates/create?barcode={barcode}&robot=BKRB0001&user_id=test",
                content_type="application/json",
            )
            assert response.status_code == HTTPStatus.BAD_REQUEST
            assert response.json == {"errors": [f"{ERROR_SAMPLES_MISSING_UUIDS} {barcode}"]}


# ---------- cherrypicked-plates/fail tests ----------


def test_fail_plate_from_barcode_bad_request_no_barcode(client):
    response = client.get("/cherrypicked-plates/fail?user_id=test_user&robot=BKRB0001&failure_type=robot_crashed")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1

    response = client.get(
        "/cherrypicked-plates/fail?user_id=test_user&robot=BKRB0001" "&failure_type=robot_crashed&barcode="
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1


def test_fail_plate_from_barcode_bad_request_no_user_id(client):
    response = client.get("/cherrypicked-plates/fail?barcode=ABC123&robot=BKRB0001&failure_type=robot_crashed")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1

    response = client.get(
        "/cherrypicked-plates/fail?barcode=ABC123&robot=BKRB0001" "&failure_type=robot_crashed&user_id="
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1


def test_fail_plate_from_barcode_bad_request_no_robot(client):
    response = client.get("/cherrypicked-plates/fail?barcode=ABC123&user_id=test_user&failure_type=robot_crashed")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1

    response = client.get(
        "/cherrypicked-plates/fail?barcode=ABC123&user_id=test_user" "&failure_type=robot_crashed&robot="
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1


def test_fail_plate_from_barcode_bad_request_no_failure_type(client):
    response = client.get("/cherrypicked-plates/fail?barcode=ABC123&user_id=test_user&robot=BKRB0001")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1

    response = client.get("/cherrypicked-plates/fail?barcode=ABC123&user_id=test_user&robot=BKRB0001&failure_type=")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1


def test_fail_plate_from_barcode_bad_request_unrecognised_failure_type(app, client):
    with app.app_context():
        failure_type = "notAFailureType"
        response = client.get(
            "/cherrypicked-plates/fail?barcode=ABC123&user_id=test_user" f"&robot=BKRB0001&failure_type={failure_type}"
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert f"'{failure_type}' is not a known cherrypicked plate failure type" in response.json["errors"]


def test_fail_plate_from_barcode_internal_server_error_constructing_message_failure(app, client):
    with app.app_context():
        with patch(
            "lighthouse.blueprints.cherrypicked_plates.construct_cherrypicking_plate_failed_message",
            side_effect=Exception(),
        ):
            response = client.get(
                "/cherrypicked-plates/fail?barcode=ABC123&user_id=test_user"
                "&robot=BKRB0001&failure_type=robot_crashed"
            )
            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert ERROR_UNEXPECTED_CHERRYPICKING_FAILURE in response.json["errors"][0]


def test_fail_plate_from_barcode_internal_server_error_constructing_message_none(app, client):
    with app.app_context():
        test_error = "this is a test error"
        with patch(
            "lighthouse.blueprints.cherrypicked_plates.construct_cherrypicking_plate_failed_message",
            return_value=([test_error], None),
        ):
            response = client.get(
                "/cherrypicked-plates/fail?barcode=ABC123&user_id=test_user&robot=BKRB0001&failure_type=robot_crashed"
            )
            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert test_error in response.json["errors"][0]


def test_fail_plate_from_barcode_internal_error_failed_broker_initialise(client):
    with patch(
        "lighthouse.blueprints.cherrypicked_plates.construct_cherrypicking_plate_failed_message"
    ) as mock_construct:
        with patch("lighthouse.blueprints.cherrypicked_plates.Broker", side_effect=Exception()):
            mock_construct.return_value = [], Message("test message content")

            response = client.get(
                "/cherrypicked-plates/fail?barcode=plate_1&user_id=test_user"
                "&robot=BKRB0001&failure_type=robot_crashed"
            )

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert ERROR_UNEXPECTED_CHERRYPICKING_FAILURE in response.json["errors"][0]


def test_fail_plate_from_barcode_internal_error_failed_broker_connect(client):
    with patch(
        "lighthouse.blueprints.cherrypicked_plates.construct_cherrypicking_plate_failed_message"
    ) as mock_construct:
        with patch("lighthouse.blueprints.cherrypicked_plates.Broker.connect", side_effect=Exception()):
            mock_construct.return_value = [], Message("test message content")

            response = client.get(
                "/cherrypicked-plates/fail?barcode=plate_1&user_id=test_user"
                "&robot=BKRB0001&failure_type=robot_crashed"
            )

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert ERROR_UNEXPECTED_CHERRYPICKING_FAILURE in response.json["errors"][0]


def test_fail_plate_from_barcode_internal_error_failed_broker_publish(client):
    with patch(
        "lighthouse.blueprints.cherrypicked_plates.construct_cherrypicking_plate_failed_message"
    ) as mock_construct:
        with patch("lighthouse.blueprints.cherrypicked_plates.Broker") as mock_broker:
            mock_broker().publish.side_effect = Exception()
            mock_construct.return_value = [], Message("test message content")

            response = client.get(
                "/cherrypicked-plates/fail?barcode=plate_1&user_id=test_user"
                "&robot=BKRB0001&failure_type=robot_crashed"
            )

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert ERROR_UNEXPECTED_CHERRYPICKING_FAILURE in response.json["errors"][0]


def test_fail_plate_from_barcode_success(client):
    with patch(
        "lighthouse.blueprints.cherrypicked_plates.construct_cherrypicking_plate_failed_message"
    ) as mock_construct:
        routing_key = "test.routing.key"
        with patch("lighthouse.blueprints.cherrypicked_plates.get_routing_key", return_value=routing_key):
            with patch("lighthouse.blueprints.cherrypicked_plates.Broker") as mock_broker:
                test_errors = ["error 1", "error 2"]
                test_message = Message("test message content")
                mock_construct.return_value = test_errors, test_message

                response = client.get(
                    "/cherrypicked-plates/fail?barcode=plate_1&user_id=test_user"
                    "&robot=BKRB0001&failure_type=robot_crashed"
                )

                mock_broker().publish.assert_called_with(test_message, routing_key)
                mock_broker().close_connection.assert_called()
                assert response.status_code == HTTPStatus.OK
                assert response.json["errors"] == test_errors
