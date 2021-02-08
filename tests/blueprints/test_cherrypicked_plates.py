import json
from http import HTTPStatus
from unittest.mock import patch

import responses
from lighthouse.messages.message import Message

# ---------- cherrypicked-plates/create tests ----------


def test_get_cherrypicked_plates_endpoint_successful(
    app,
    client,
    dart_samples_for_bp_test,
    samples_with_lab_id,
    mocked_responses,
    mlwh_lh_samples,
    source_plates,
):
    with patch(
        "lighthouse.blueprints.cherrypicked_plates.add_cog_barcodes",
        return_value="TS1",
    ):
        ss_url = f"http://{app.config['SS_HOST']}/api/v2/heron/plates"

        body = json.dumps({"barcode": "plate_1"})
        mocked_responses.add(
            responses.POST,
            ss_url,
            body=body,
            status=HTTPStatus.OK,
        )
        response = client.get(
            "/cherrypicked-plates/create?barcode=plate_1&robot=BKRB0001&user_id=test",
            content_type="application/json",
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json == {"data": {"plate_barcode": "plate_1", "centre": "TS1", "number_of_positives": 2}}


def test_get_cherrypicked_plates_endpoint_no_barcode_in_request(app, client, samples_with_lab_id):
    response = client.get(
        "/cherrypicked-plates/create?user_id=test&robot=BKRB0001",
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["GET request needs 'barcode' in url"]}


def test_get_cherrypicked_plates_endpoint_no_robot_number_in_request(app, client, samples_with_lab_id):
    response = client.get(
        "/cherrypicked-plates/create?barcode=plate_1&user_id=test",
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["GET request needs 'robot' in url"]}


def test_get_cherrypicked_plates_endpoint_no_user_id_in_request(app, client, samples_with_lab_id):
    response = client.get(
        "/cherrypicked-plates/create?barcode=plate_1&robot=1234",
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["GET request needs 'user_id' in url"]}


def test_get_cherrypicked_plates_endpoint_add_cog_barcodes_failed(
    app, client, dart_samples_for_bp_test, samples_with_lab_id, centres, mocked_responses
):
    baracoda_url = f"http://{app.config['BARACODA_URL']}/barcodes_group/TS1/new?count=2"

    mocked_responses.add(
        responses.POST,
        baracoda_url,
        status=HTTPStatus.BAD_REQUEST,
    )

    response = client.get(
        "/cherrypicked-plates/create?barcode=plate_1&robot=BKRB0001&user_id=test",
        content_type="application/json",
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["Failed to add COG barcodes to plate: plate_1"]}


def test_get_cherrypicked_plates_endpoint_ss_failure(
    app, client, dart_samples_for_bp_test, samples_with_lab_id, mocked_responses, source_plates
):
    with patch(
        "lighthouse.blueprints.cherrypicked_plates.add_cog_barcodes",
        return_value="TS1",
    ):
        ss_url = f"http://{app.config['SS_HOST']}/api/v2/heron/plates"

        body = json.dumps({"errors": ["The barcode 'plate_1' is not a recognised format."]})
        mocked_responses.add(
            responses.POST,
            ss_url,
            body=body,
            status=HTTPStatus.UNPROCESSABLE_ENTITY,
        )

        response = client.get(
            "/cherrypicked-plates/create?barcode=plate_1&robot=BKRB0001&user_id=test",
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json == {"errors": ["The barcode 'plate_1' is not a recognised format."]}


def test_get_cherrypicked_plates_mlwh_update_failure(
    app, client, dart_samples_for_bp_test, samples_with_lab_id, mocked_responses, source_plates
):
    with patch(
        "lighthouse.blueprints.cherrypicked_plates.add_cog_barcodes",
        return_value="TS1",
    ):
        with patch(
            "lighthouse.blueprints.cherrypicked_plates.update_mlwh_with_cog_uk_ids",
            side_effect=Exception("Boom!"),
        ):
            ss_url = f"http://{app.config['SS_HOST']}/api/v2/heron/plates"

            body = json.dumps({"barcode": "plate_1"})
            mocked_responses.add(
                responses.POST,
                ss_url,
                body=body,
                status=HTTPStatus.OK,
            )

            response = client.get(
                "/cherrypicked-plates/create?barcode=plate_1&robot=BKRB0001&user_id=test",
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


def test_post_plates_endpoint_mismatched_sample_numbers(app, client, dart_samples_for_bp_test, samples_with_lab_id):
    with patch(
        "lighthouse.blueprints.cherrypicked_plates.add_cog_barcodes",
        return_value="TS1",
    ):
        with patch(
            "lighthouse.blueprints.cherrypicked_plates.check_matching_sample_numbers",
            return_value=False,
        ):
            barcode = "plate_1"
            response = client.get(
                f"/cherrypicked-plates/create?barcode={barcode}&robot=BKRB0001&user_id=test",
                content_type="application/json",
            )

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert response.json == {
                "errors": [f"Mismatch in destination and source sample data for plate '{barcode}'"]
            }


def test_post_cherrypicked_plates_endpoint_missing_dart_data(app, client):
    with patch(
        "lighthouse.blueprints.cherrypicked_plates.find_dart_source_samples_rows",
        return_value=[],
    ):
        barcode = "plate_1"
        response = client.get(
            "/cherrypicked-plates/create?barcode=plate_1&robot=BKRB0001&user_id=test",
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert response.json == {"errors": ["Failed to find sample data in DART for plate barcode: " + barcode]}


def test_post_cherrypicked_plates_endpoint_missing_source_plate_uuids(
    app, client, dart_samples_for_bp_test, samples_with_lab_id
):
    with patch(
        "lighthouse.blueprints.cherrypicked_plates.add_cog_barcodes",
        return_value="TS1",
    ):
        with patch(
            "lighthouse.blueprints.cherrypicked_plates.get_source_plates_for_samples",
            return_value=[],
        ):
            barcode = "plate_1"
            response = client.get(
                f"/cherrypicked-plates/create?barcode={barcode}&robot=BKRB0001&user_id=test",
                content_type="application/json",
            )
            assert response.status_code == HTTPStatus.BAD_REQUEST
            assert response.json == {"errors": ["No source plate UUIDs for samples of destination plate: " + barcode]}


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
        errors = response.json["errors"]
        assert len(errors) == 1
        assert f"'{failure_type}' is not a known cherrypicked plate failure type" in errors


def test_fail_plate_from_barcode_internal_server_error_constructing_message_failure(app, client):
    with app.app_context():
        with patch(
            "lighthouse.blueprints.cherrypicked_plates.construct_cherrypicking_plate_failed_message",  # noqa: E501
            side_effect=Exception("Boom!"),
        ):
            response = client.get(
                "/cherrypicked-plates/fail?barcode=ABC123&user_id=test_user"
                "&robot=BKRB0001&failure_type=robot_crashed"
            )
            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert len(response.json["errors"]) == 1
            assert (
                "An unexpected error occurred attempting to record cherrypicking plate failure"
                in response.json["errors"][0]
            )


def test_fail_plate_from_barcode_internal_server_error_constructing_message_none(app, client):
    with app.app_context():
        test_error = "this is a test error"
        with patch(
            "lighthouse.blueprints.cherrypicked_plates.construct_cherrypicking_plate_failed_message",  # noqa: E501
            return_value=([test_error], None),
        ):
            response = client.get(
                "/cherrypicked-plates/fail?barcode=ABC123&user_id=test_user"
                "&robot=BKRB0001&failure_type=robot_crashed"
            )
            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert len(response.json["errors"]) == 1
            assert test_error in response.json["errors"][0]


def test_fail_plate_from_barcode_internal_error_failed_broker_initialise(client):
    with patch(
        "lighthouse.blueprints.cherrypicked_plates.construct_cherrypicking_plate_failed_message"
    ) as mock_construct:
        with patch("lighthouse.blueprints.cherrypicked_plates.Broker", side_effect=Exception("Boom!")):
            mock_construct.return_value = [], Message("test message content")

            response = client.get(
                "/cherrypicked-plates/fail?barcode=plate_1&user_id=test_user"
                "&robot=BKRB0001&failure_type=robot_crashed"
            )

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert len(response.json["errors"]) == 1
            assert (
                "An unexpected error occurred attempting to record cherrypicking plate failure"
                in response.json["errors"][0]
            )


def test_fail_plate_from_barcode_internal_error_failed_broker_connect(client):
    with patch(
        "lighthouse.blueprints.cherrypicked_plates.construct_cherrypicking_plate_failed_message"
    ) as mock_construct:
        with patch(
            "lighthouse.blueprints.cherrypicked_plates.Broker.connect",
            side_effect=Exception("Boom!"),
        ):
            mock_construct.return_value = [], Message("test message content")

            response = client.get(
                "/cherrypicked-plates/fail?barcode=plate_1&user_id=test_user"
                "&robot=BKRB0001&failure_type=robot_crashed"
            )

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert (
                "An unexpected error occurred attempting to record cherrypicking plate failure"
                in response.json["errors"][0]
            )


def test_fail_plate_from_barcode_internal_error_failed_broker_publish(client):
    with patch(
        "lighthouse.blueprints.cherrypicked_plates.construct_cherrypicking_plate_failed_message"
    ) as mock_construct:
        with patch("lighthouse.blueprints.cherrypicked_plates.Broker") as mock_broker:
            mock_broker().publish.side_effect = Exception("Boom!")
            mock_construct.return_value = [], Message("test message content")

            response = client.get(
                "/cherrypicked-plates/fail?barcode=plate_1&user_id=test_user"
                "&robot=BKRB0001&failure_type=robot_crashed"
            )

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert (
                "An unexpected error occurred attempting to record cherrypicking plate failure"
                in response.json["errors"][0]
            )


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
