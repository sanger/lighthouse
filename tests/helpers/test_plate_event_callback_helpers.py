from unittest.mock import patch

from lighthouse.helpers.plate_event_callbacks import fire_callbacks


def test_fire_callbacks_unrecognised_event(app, message_unknown):
    with app.app_context():
        success, errors = fire_callbacks(message_unknown)

        assert len(errors) == 0
        assert success is True


def test_fire_callbacks_with_failure(app, message_source_all_negative):
    with app.app_context():
        with patch(
            "lighthouse.helpers.plate_event_callbacks.set_locations_in_labwhere",
            side_effect=Exception("Labwhere was down"),
        ):
            success, errors = fire_callbacks(message_source_all_negative)

            assert len(errors) == 1
            assert errors[0] == "Exception: Labwhere was down"
            assert success is False


def test_fire_callbacks_source_all_negatives(app, message_source_all_negative):
    with app.app_context():
        with patch(
            "lighthouse.helpers.plate_event_callbacks.set_locations_in_labwhere"
        ) as mock_set_locations_in_labwhere:
            success, errors = fire_callbacks(message_source_all_negative)

            mock_set_locations_in_labwhere.assert_called_with(
                labware_barcodes=["plate-barcode"],
                location_barcode="heron-bin",
                user_barcode="robot-serial",
            )

            assert len(errors) == 0
            assert success is True


def test_fire_callbacks_source_fully_picked(app, message_source_complete):
    with app.app_context():
        with patch(
            "lighthouse.helpers.plate_event_callbacks.set_locations_in_labwhere"
        ) as mock_set_locations_in_labwhere:
            success, errors = fire_callbacks(message_source_complete)

            mock_set_locations_in_labwhere.assert_called_with(
                labware_barcodes=["plate-barcode"],
                location_barcode="heron-bin",
                user_barcode="robot-serial",
            )

            assert len(errors) == 0
            assert success is True


# TODO: test_fire_callbacks_control_plate_used
#       It is currently unclear which event to use for this.
#       We *Could* use the destination complete event, and extract
#       the information from the control sample friendly name but
#       there may be a more robust approach
