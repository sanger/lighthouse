from http import HTTPStatus
from unittest.mock import patch
from uuid import uuid4

import pytest

from lighthouse.classes.beckman_v3 import Beckman

CACHE = {}


def int_to_uuid(value: int) -> str:
    if value not in CACHE:
        CACHE[value] = str(uuid4())
    return CACHE[value]


def test_event_source_no_pickable_wells_missing_barcode(
    app,
    client,
    clear_events,
):
    with app.app_context():
        response = client.get(
            "/v1/plate-events/create?barcode=&event_type="
            + Beckman.EVENT_SOURCE_ALL_NEGATIVES
            + "&robot=BKRB0001&user_id=RC34",
        )

        response_errors = response.json.get("_issues")
        assert "'barcode' should not be an empty string" in response_errors.get("plate_barcode")


@pytest.mark.parametrize("source_barcode", ["GLS-GP-016240"])
@pytest.mark.parametrize("robot", ["BKRB0001"])
@pytest.mark.parametrize("user_id", ["LT1"])
def test_get_event_source_no_pickable_wells(
    app,
    client,
    clear_events,
    mocked_rabbit_channel,
    positive_samples_in_source_plate,
    source_barcode,
    robot,
    user_id,
    mocked_responses,
):
    with app.app_context():
        with patch(
            "lighthouse.hooks.beckman_events.uuid4",
            side_effect=[int_to_uuid(1)],
        ):
            with patch(
                "lighthouse.classes.events.PlateEvent.message_timestamp",
                "mytime",
            ):
                with patch(
                    "lighthouse.classes.services.mongo.MongoServiceMixin.get_source_plate_uuid",
                    side_effect=[int_to_uuid(2)],
                ):
                    with patch(
                        "lighthouse.classes.services.mongo.MongoServiceMixin.get_positive_samples_in_source_plate",
                        return_value=positive_samples_in_source_plate,
                    ):
                        with patch("lighthouse.classes.services.labwhere.set_locations_in_labwhere") as mocked_labwhere:
                            response = client.get(
                                "/v1/plate-events/create?barcode="
                                + source_barcode
                                + "&event_type="
                                + Beckman.EVENT_SOURCE_ALL_NEGATIVES
                                + "&robot="
                                + robot
                                + "&user_id="
                                + user_id,
                            )

                    # Test the event is created
                    assert response.status_code == HTTPStatus.OK

                    mocked_rabbit_channel.basic_publish.assert_called_with(
                        exchange="lighthouse.test.examples",
                        routing_key=f"test.event.{ Beckman.EVENT_SOURCE_ALL_NEGATIVES }",
                        body='{"event": {"uuid": "'
                        + int_to_uuid(1)
                        + (
                            '", "event_type": "' + Beckman.EVENT_SOURCE_ALL_NEGATIVES + '", '
                            '"occured_at": "mytime", "user_identifier": "' + user_id + '", "subjects": '
                            '[{"role_type": "sample", "subject_type": "sample", "friendly_name": '
                            '"sample_001__rna_1__lab_1__Positive", "uuid": "0a53e7b6-7ce8-4ebc-95c3-02dd64942531"}, '
                            '{"role_type": "cherrypicking_source_labware", "subject_type": "plate", '
                            '"friendly_name": "' + source_barcode + '", "uuid": "' + int_to_uuid(2) + '"}, '
                            '{"role_type": "robot", "subject_type": "robot", "friendly_name": "' + robot + '", '
                            '"uuid": "082effc3-f769-4e83-9073-dc7aacd5f71b"}], '
                            '"metadata": {"source_plate_barcode": "' + source_barcode + '"}}, "lims": "LH_TEST"}'
                        ),
                    )

                    mocked_labwhere.assert_called_once_with(
                        labware_barcodes=[source_barcode],
                        location_barcode=app.config["LABWHERE_DESTROYED_BARCODE"],
                        user_barcode=robot,
                    )
